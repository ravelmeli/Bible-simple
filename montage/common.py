"""Shared helpers for the 9:16 shorts (retention-focused style).

A short is a list of scenes. Each scene has a decor, elements and « beats » (keyword cards, rings, stamps)
that are timed on the word-level transcript, so the picture reacts to the voice. Running text is carried by
the captions only; cards stay short (a keyword or a reference) so nothing is read twice.
"""
import json
import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

SFX_FILES = {
    "hit": ("assets/audio/hit.wav", 1.1),
    "riser": ("assets/audio/riser.wav", 1.4),
    "tick": ("assets/audio/tick.wav", 0.09),
    "whoosh": (".media/audio/sfx/sfx_004.mp3", 2.0),
    "mer": (".media/audio/sfx/sfx_002.mp3", 9.4),
    "impact": (".media/audio/sfx/sfx_001.mp3", 2.0),
}
SFX_VOL = {"hit": 0.5, "riser": 0.24, "tick": 0.22, "whoosh": 0.14, "mer": 0.07, "impact": 0.7}
SFX_SCALE = 0.6  # keeps effects under the voice (voice-only mix is about -19 LUFS)

HOW = {
    "rise": ("opacity: 0, y: 90", 'opacity: 1, y: 0, duration: 0.8, ease: "power3.out"'),
    "pop": ("opacity: 0, scale: 0.5", 'opacity: 1, scale: 1, duration: 0.42, ease: "back.out(2.4)"'),
    "slamL": ("opacity: 0, x: -260", 'opacity: 1, x: 0, duration: 0.45, ease: "power4.out"'),
    "slamR": ("opacity: 0, x: 260", 'opacity: 1, x: 0, duration: 0.45, ease: "power4.out"'),
    "drop": ("opacity: 0, y: -160, scale: 1.3", 'opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "power4.in"'),
    "fade": ("opacity: 0", 'opacity: 1, duration: 0.4, ease: "power1.out"'),
    "cut": ("opacity: 0", 'opacity: 1, duration: 0.01'),
}


def norm(w):
    return re.sub(r"[\.,\?!:;«»\"'’() ]", "", w).lower().strip()


class Short:
    def __init__(self, project_dir, duration, fixes=None):
        self.dir = project_dir
        self.duration = duration
        self.scenes = []
        self.tweens = []
        self.audio = []
        self._uid = 0
        words = json.load(open(os.path.join(project_dir, "transcript.json")))
        fixes = fixes or {}
        for w in words:
            w["text"] = fixes.get(w["text"], w["text"])
        self.words = words

    # ---------- transcript ----------
    def t(self, word, n=0, end=False):
        """Start (or end) time of the n-th occurrence of `word` in the voice-over."""
        hits = [w for w in self.words if norm(w["text"]) == norm(word)]
        if n >= len(hits):
            raise KeyError(f"word {word!r} occurrence {n} not found")
        return hits[n]["end" if end else "start"]

    def phrase(self, *words, end=False):
        """Time of a consecutive word sequence (first word start, or last word end)."""
        seq = [norm(w) for w in words]
        for i in range(len(self.words) - len(seq) + 1):
            if [norm(x["text"]) for x in self.words[i:i + len(seq)]] == seq:
                return self.words[i + len(seq) - 1]["end"] if end else self.words[i]["start"]
        raise KeyError(f"phrase {words!r} not found")

    # ---------- primitives ----------
    def uid(self):
        self._uid += 1
        return f"e{self._uid}"

    def tween(self, sel, frm, to, at):
        self.tweens.append(f'tl.fromTo("{sel}", {{ {frm} }}, {{ {to} }}, {at:.3f});')

    def sfx(self, kind, at, vol=None):
        path, dur = SFX_FILES[kind]
        v = round((SFX_VOL[kind] if vol is None else vol) * SFX_SCALE, 3)
        n = len([a for a in self.audio if a[0].startswith(f"sfx-{kind}")])
        dur = min(dur, max(self.duration - at, 0.05))
        self.audio.append((f"sfx-{kind}-{n}", path, round(at, 3), round(dur, 3), v))

    def flash(self, at, color="gold", strength=0.35):
        rgba = {"gold": "246, 215, 127", "red": "139, 46, 31", "white": "255, 248, 230"}[color]
        self.tweens.append(
            f'tl.fromTo("#flash", {{ opacity: {strength}, backgroundColor: "rgba({rgba}, 1)" }}, '
            f'{{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {at:.3f});')

    def punch(self, scene_id, at, amount=1.035):
        self.tweens.append(
            f'tl.fromTo("#{scene_id} .bgset", {{ scale: 1 }}, {{ scale: {amount}, duration: 0.09, yoyo: true, repeat: 1, ease: "power2.out" }}, {at:.3f});')

    # ---------- scene ----------
    def scene(self, sid, start, end, decor, pan=(0, 0), zoom=(1.05, 1.14), dark=0.0):
        sc = Scene(self, sid, start, end, decor, pan, zoom, dark)
        self.scenes.append(sc)
        return sc

    # ---------- captions ----------
    def captions(self, suppress=(), max_words=4, y_class="cap"):
        words = [dict(w) for w in self.words]
        for w in words:
            if w["text"].endswith("?") and not w["text"].endswith(" ?"):
                w["text"] = w["text"][:-1] + " ?"
            if w["text"].endswith(":") and not w["text"].endswith(" :"):
                w["text"] = w["text"][:-1] + " :"
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if w["text"].rstrip().endswith((".", "?", "!", ",", ":")) or len(cur) == max_words:
                chunks.append(cur)
                cur = []
        if cur:
            chunks.append(cur)
        html, tw = [], []
        for n, ch in enumerate(chunks):
            start = ch[0]["start"]
            nxt = chunks[n + 1][0]["start"] if n + 1 < len(chunks) else self.duration
            end = min(max(ch[-1]["end"] + 0.22, start + 0.55), nxt)
            if any(a - 0.05 <= start and ch[-1]["end"] <= b + 0.35 for a, b in suppress):
                continue
            spans = " ".join(f'<span class="cw cw{n}-{k}">{w["text"]}</span>' for k, w in enumerate(ch))
            html.append(f'<p class="clip {y_class}" id="cap{n}" data-start="{start:.3f}" data-duration="{end - start:.3f}">'
                        f'<span class="capin" id="capin{n}">{spans}</span></p>')
            tw.append(f'tl.fromTo("#capin{n}", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {start:.3f});')
            for k, w in enumerate(ch):
                s, e = w["start"], max(w["end"], w["start"] + 0.16)
                tw.append(f'tl.fromTo(".cw{n}-{k}", {{ color: "#f4ead2", scale: 1 }}, {{ color: "#f6d77f", scale: 1.06, duration: 0.09, ease: "power2.out" }}, {s:.3f});')
                tw.append(f'tl.to(".cw{n}-{k}", {{ color: "#f4ead2", scale: 1, duration: 0.14 }}, {e:.3f});')
        return html, tw

    # ---------- assemble ----------
    def build(self, template_path, out_path="index.html", suppress=()):
        fade = 0.3
        scene_html, scene_tw = [], []
        for i, sc in enumerate(self.scenes):
            s = max(0, sc.start - (fade / 2 if i else 0))
            e = min(self.duration, sc.end + (fade / 2 if i < len(self.scenes) - 1 else 0))
            dur = round(e - s, 3)
            scene_html.append(sc.render(s, dur))
            dx, dy = sc.pan
            z0, z1 = sc.zoom
            scene_tw.append(
                f'tl.fromTo("#{sc.id} .bgimg", {{ scale: {z0}, x: 0, y: 0 }}, '
                f'{{ scale: {z1}, x: {dx}, y: {dy}, duration: {dur}, ease: "none" }}, {s:.3f});')
            if i:
                scene_tw.append(f'tl.fromTo("#{sc.id} .sc-in", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade}, ease: "none" }}, {s:.3f});')
        cap_html, cap_tw = self.captions(suppress=suppress)
        audio = [("voix", "assets/voix.wav", 0, self.duration, 1)] + self.audio
        audio_html = "\n      ".join(
            f'<audio id="{a}" src="{src}" data-start="{st}" data-duration="{d}" data-volume="{v}"></audio>'
            for a, src, st, d, v in audio)
        motes = "".join(
            f'<i class="mote" style="left:{(i * 137) % 1000 + 40}px;top:{(i * 263) % 1700 + 100}px;'
            f'width:{3 + (i * 7) % 5}px;height:{3 + (i * 7) % 5}px;opacity:{0.2 + ((i * 11) % 5) * 0.07:.2f}"></i>'
            for i in range(18))
        mote_tw = (f'gsap.utils.toArray(".mote").forEach((m, i) => {{ tl.fromTo(m, {{ y: 0, x: 0 }}, '
                   f'{{ y: -240 - (i % 4) * 60, x: ((i % 3) - 1) * 50, duration: {self.duration}, ease: "none" }}, 0); }});')
        progress_tw = f'tl.fromTo("#progress i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {self.duration}, ease: "none" }}, 0);'
        template = open(template_path).read()
        out = (template.replace("{{DURATION}}", str(self.duration))
               .replace("{{SCENES}}", "\n      ".join(scene_html))
               .replace("{{CAPTIONS}}", "\n      ".join(cap_html))
               .replace("{{AUDIO}}", audio_html)
               .replace("{{MOTES}}", motes)
               .replace("{{TWEENS}}", "\n      ".join(scene_tw + self.tweens + cap_tw + [mote_tw, progress_tw])))
        open(os.path.join(self.dir, out_path), "w").write(out)
        print(f"scenes: {len(self.scenes)}  captions: {len(cap_html)}  sfx/audio: {len(audio)}  tweens: {len(self.tweens) + len(cap_tw) + len(scene_tw)}")


class Scene:
    def __init__(self, short, sid, start, end, decor, pan, zoom, dark):
        self.short, self.id, self.start, self.end = short, sid, start, end
        self.decor, self.pan, self.zoom, self.dark = decor, pan, zoom, dark
        self.html = []

    def render(self, s, dur):
        veil = f'<div class="veil" style="opacity:{self.dark}"></div>' if self.dark else ""
        return (f'<div class="clip scene" id="{self.id}" data-start="{s:.3f}" data-duration="{dur}">'
                f'<div class="sc-in"><div class="bgset"><img class="bgimg" src="assets/decors/{self.decor}.jpg" />'
                f'{veil}</div>'
                + "".join(self.html) + "</div></div>")

    def _anim(self, sel, at, how, rot=None):
        frm, to = HOW[how]
        if rot is not None:
            frm += f", rotation: {rot - 5}"
            to += f", rotation: {rot}"
        self.short.tween(sel, frm, to, at)

    def element(self, name, h, style, at, how="rise", z=5, fade_bottom=False):
        w0, h0 = Image.open(os.path.join(self.short.dir, "assets/elements", name + ".png")).size
        w = round(w0 * h / h0)
        i = self.short.uid()
        mask = "-webkit-mask-image:linear-gradient(to bottom,#000 80%,transparent 100%);mask-image:linear-gradient(to bottom,#000 80%,transparent 100%);" if fade_bottom else ""
        self.html.append(f'<img class="el" id="{i}" src="assets/elements/{name}.png" style="width:{w}px;height:{h}px;z-index:{z};{mask}{style}" />')
        self._anim(f"#{i}", at, how)
        return i

    def image(self, name, w, h, style, at, how="rise", z=5, cls="el"):
        i = self.short.uid()
        self.html.append(f'<img class="{cls}" id="{i}" src="assets/elements/{name}.png" style="width:{w}px;height:{h}px;z-index:{z};{style}" />')
        self._anim(f"#{i}", at, how)
        return i

    def kw(self, text, style, at, how="pop", rot=0, hero=False, tick=True, cls=""):
        i = self.short.uid()
        base = "hero" if hero else "kw"
        self.html.append(f'<div class="{base} {cls}" id="{i}" style="{style}"><span>{text}</span></div>')
        self._anim(f"#{i}", at, how, rot)
        if tick:
            self.short.sfx("tick", at)
        return i

    def ref(self, text, style, at, how="slamL"):
        i = self.short.uid()
        self.html.append(f'<div class="refchip" id="{i}" style="{style}"><span>{text}</span></div>')
        self._anim(f"#{i}", at, how)
        return i

    def ring(self, cx, cy, r, at, color="#8b2e1f", dur=0.9, hold=True):
        i = self.short.uid()
        d = 2 * r + 40
        self.html.append(
            f'<svg class="ring" id="{i}" style="left:{cx - d // 2}px;top:{cy - d // 2}px;width:{d}px;height:{d}px" viewBox="0 0 {d} {d}">'
            f'<circle cx="{d // 2}" cy="{d // 2}" r="{r}" stroke="{color}" transform="rotate(-90 {d // 2} {d // 2})" /></svg>')
        self.short.tween(f"#{i} circle", "strokeDashoffset: 1000, opacity: 1", f'strokeDashoffset: 0, duration: {dur}, ease: "power2.inOut"', at)
        self.short.tween(f"#{i}", "opacity: 0", 'opacity: 1, duration: 0.05', at)
        self.short.tween(f"#{i}", "scale: 1", 'scale: 1.08, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut"', at + dur)
        return i

    def strike_line(self, x1, y1, x2, y2, at, color="#8b2e1f", width=14, dur=0.28):
        i = self.short.uid()
        self.html.append(
            f'<svg class="strikeline" id="{i}" viewBox="0 0 1080 1920"><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" /></svg>')
        length = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) + 4
        self.short.tween(f"#{i} line", f"strokeDasharray: {length}, strokeDashoffset: {length}", f'strokeDashoffset: 0, duration: {dur}, ease: "power3.out"', at)
        return i

    def raw(self, html):
        self.html.append(html)
