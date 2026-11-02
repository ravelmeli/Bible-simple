// Audit des chevauchements : aucun élément ne doit en cacher un autre (texte, carte, citation, autocollant, titre, sous-titre).
// Usage : node audit_chevauchements.js <dossier-projet> [pas en secondes, défaut 0.5] [aire minimale px², défaut 1200]
// Charge index.html dans Chromium, positionne la timeline GSAP à chaque instant et compare les rectangles à l'écran des
// éléments visibles (opacité > 0,35). Les décors d'animation (vent, souffle, lueur, anneau, éclat, flèche, poussière) sont ignorés.
// Sortie : une ligne par paire qui se chevauche, regroupée par paire d'éléments (première et dernière seconde du conflit).
const path = require("path");
const { chromium } = require("/opt/node-tools/node_modules/playwright");

const dir = path.resolve(process.argv[2] || ".");
const step = parseFloat(process.argv[3] || "0.5");
const minArea = parseFloat(process.argv[4] || "1200");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  // GSAP vient d'un CDN dans index.html : on le sert depuis le dossier local de HyperFrames (hors ligne).
  const gsapLocal = require("child_process").execSync("find / -name gsap.min.js -not -path '/proc/*' 2>/dev/null | head -1").toString().trim();
  await page.route(/gsap.*\.min\.js/, (route) => route.fulfill({ path: gsapLocal, contentType: "application/javascript" }));
  await page.addInitScript(() => { window.__timelines = window.__timelines || {}; });
  page.on("pageerror", (e) => console.error("pageerror:", String(e).slice(0, 200)));
  await page.goto("file://" + path.join(dir, "index.html"));
  for (let k = 0; k < 100; k++) {
    if (await page.evaluate(() => !!(window.__timelines && window.__timelines.main))) break;
    await page.waitForTimeout(300);
  }
  await page.evaluate(() => document.fonts.ready);
  const dur = await page.evaluate(() => window.__timelines.main.duration());
  const pairs = new Map();
  const vide = [];
  const KIND = [["headline", "titre"], ["kq", "citation"], ["card", "carte"], ["tag", "bandeau"], ["label", "étiquette"], ["stamp", "tampon"],
    ["teaser", "teaser"], ["sticker", "autocollant"], ["word", "mot"], ["counter", "compteur"], ["cta", "cta"], ["ref", "référence"], ["box", "boîte"], ["wind", "vent"], ["breath", "souffle"]];
  for (let t = 0.5; t < dur; t += step) {
    const found = await page.evaluate((t) => {
      const tl = window.__timelines.main;
      tl.seek(t, false);
      const out = [];
      const vis = (el) => {
        let o = 1;
        for (let e = el; e && e.nodeType === 1; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity);
        return o;
      };
      for (const el of document.querySelectorAll(".node")) {
        const c = el.className.baseVal !== undefined ? el.className.baseVal : el.className;
        if (/\b(route|lead|glow|burst|ring|arrow)\b/.test(c)) continue;
        if (vis(el) < 0.35) continue;
        let r = el.getBoundingClientRect();
        if (/\b(wind|breath)\b/.test(c)) {
          // seuls les traits réellement visibles comptent (le conteneur est toujours là)
          let l = 1e9, tp = 1e9, rr = -1e9, bt = -1e9;
          for (const d of el.querySelectorAll("path")) {
            if (vis(d) < 0.3) continue;
            const q = d.getBoundingClientRect();
            l = Math.min(l, q.left); tp = Math.min(tp, q.top); rr = Math.max(rr, q.right); bt = Math.max(bt, q.bottom);
          }
          if (l > 1e8) continue;
          r = { left: l, top: tp, width: rr - l, height: bt - tp };
        }
        if (/\bheadline\b/.test(c)) {
          // le bloc du titre occupe toute la largeur : on mesure l'emprise réelle du texte
          let l = 1e9, tp = 1e9, rr = -1e9, bt = -1e9;
          for (const d of el.querySelectorAll(".kick, .h > div, .sub")) {
            const g = document.createRange();
            g.selectNodeContents(d);
            for (const q of g.getClientRects()) { if (q.width < 2) continue; l = Math.min(l, q.left); tp = Math.min(tp, q.top); rr = Math.max(rr, q.right); bt = Math.max(bt, q.bottom); }
          }
          if (l < 1e8) r = { left: l, top: tp, width: rr - l, height: bt - tp };
        }
        if (r.width < 8 || r.height < 8) continue;
        if (r.left + r.width < 0 || r.left > 1920 || r.top + r.height < 0 || r.top > 1080) continue; // hors écran
        const sc = el.offsetWidth ? el.getBoundingClientRect().width / el.offsetWidth : 1;
        if (sc < 0.75 && /\b(sticker|headline|tag|kq|card|stamp|word|label)\b/.test(c) && sc > 0) { if (!window.__zo) window.__zo = {}; }
        out.push({ sc, id: el.id, c, x: r.left, y: r.top, w: r.width, h: r.height, txt: (el.innerText || "").replace(/\s+/g, " ").slice(0, 28) });
      }
      for (const el of document.querySelectorAll(".clip.cap")) {
        const s = parseFloat(el.dataset.start), d = parseFloat(el.dataset.duration);
        if (t < s || t >= s + d) continue;
        const inner = el.querySelector(".capin") || el;
        const r = inner.getBoundingClientRect();
        if (r.width > 8) out.push({ id: el.id, c: "caption", x: r.left, y: r.top, w: r.width, h: r.height, txt: (el.innerText || "").slice(0, 28) });
      }
      return out;
    }, t);
    // plans vides : rien à l'écran hormis le titre et les sous-titres
    const contenu = found.filter((e) => !/\b(headline)\b/.test(e.c) && e.c !== "caption" && !/\b(wind|breath)\b/.test(e.c));
    if (contenu.length === 0) { vide.push(t); }
    // vue d'ensemble (caméra dézoomée) : plusieurs plans à l'écran, on ne contrôle pas
    const scs = found.filter((e) => /\b(tag|kq|card|headline)\b/.test(e.c)).map((e) => e.sc);
    if (scs.length && Math.min(...scs) < 0.7) continue;
    for (let i = 0; i < found.length; i++) {
      for (let j = i + 1; j < found.length; j++) {
        const a = found[i], b = found[j];
        const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
        const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
        if (ox <= 0 || oy <= 0 || ox * oy < minArea) continue;
        const kind = (e) => (KIND.find(([k]) => new RegExp("\\b" + k + "\\b").test(e.c)) || [0, e.c])[1];
        // vent / souffle dessinés : on ne signale que ceux qui passent sous ou sur un texte
        const isDecor = (e) => /\b(wind|breath)\b/.test(e.c);
        const isText = (e) => /\b(headline|kq|card|tag|label|stamp|teaser|word|counter|cta|ref|box)\b/.test(e.c) || e.c === "caption";
        if ((isDecor(a) && !isText(b)) || (isDecor(b) && !isText(a)) || (isDecor(a) && isDecor(b))) continue;
        const key = a.id + "|" + b.id;
        let p = pairs.get(key);
        if (!p || t - p.t1 > step * 1.6) {
          p = { a, b, ka: kind(a), kb: kind(b), t0: t, t1: t, area: 0 };
          pairs.set(key + "@" + t, p);
          pairs.set(key, p);
        }
        p.t1 = t;
        p.area = Math.max(p.area, Math.round(ox * oy));
      }
    }
  }
  await browser.close();
  const list = [...new Set(pairs.values())].sort((p, q) => p.t0 - q.t0);
  for (const p of list) {
    // pop d'entrée d'un autocollant (rebond 0,7 s) : chevauchement bref et petit, ignoré
    if (p.t1 - p.t0 < 1.2 && p.area < 12000 && !process.argv.includes("--tout")) continue;
    console.log(`${p.t0.toFixed(1)}–${p.t1.toFixed(1)} s  ${p.ka} « ${p.a.txt} » (${p.a.id})  ×  ${p.kb} « ${p.b.txt} » (${p.b.id})  ${p.area} px²`);
  }
  let run = null;
  const runs = [];
  for (const t of vide) { if (run && t - run[1] <= step * 1.6) run[1] = t; else { run = [t, t]; runs.push(run); } }
  for (const [a, b] of runs) if (b - a + step >= 3) console.log(`VIDE ${a.toFixed(1)}–${(b + step).toFixed(1)} s : rien d'autre que le titre et les sous-titres`);
  console.log(list.length ? `${list.length} chevauchement(s)` : "Aucun chevauchement.");
})();
