<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>La Bible Simple - Short</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {
        font-family: "Cormorant Garamond";
        src: url("assets/fonts/CormorantGaramond.ttf") format("truetype");
        font-weight: 300 700;
        font-style: normal;
      }
      @font-face {
        font-family: "Cormorant Garamond";
        src: url("assets/fonts/CormorantGaramond-Italic.ttf") format("truetype");
        font-weight: 300 700;
        font-style: italic;
      }
      @font-face {
        font-family: "EB Garamond";
        src: url("assets/fonts/EBGaramond.ttf") format("truetype");
        font-weight: 400 800;
        font-style: normal;
      }
      @font-face {
        font-family: "Frank Ruhl Libre";
        src: url("assets/fonts/FrankRuhlLibre.ttf") format("truetype");
        font-weight: 300 900;
        font-style: normal;
      }

      html, body { margin: 0; background: #1a1410; }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        font-family: "Cormorant Garamond", Georgia, serif;
        color: #1a1410;
      }

      /* ---------- scene ---------- */
      .sc-in { position: absolute; inset: 0; }
      .bgset { position: absolute; inset: 0; overflow: hidden; }
      .bgimg {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .bgimg { filter: sepia(0.3) saturate(1.2) contrast(1.08) brightness(1.0); }
      .bgset::after {
        content: "";
        position: absolute;
        inset: 0;
        background: url("assets/decors/parchemin.jpg") center / cover;
        mix-blend-mode: multiply;
        opacity: 0.42;
      }
      .bgset::before {
        content: "";
        position: absolute;
        inset: 0;
        z-index: 2;
        background: radial-gradient(ellipse 85% 70% at 50% 45%, rgba(26, 20, 16, 0) 50%, rgba(26, 20, 16, 0.68) 100%);
      }
      .veil { position: absolute; inset: 0; background: #1a1410; }

      .el {
        position: absolute;
        filter: drop-shadow(16px 24px 24px rgba(26, 20, 16, 0.55)) sepia(0.1);
      }

      /* ---------- keyword cards and chips ---------- */
      .kw, .hero, .refchip, .ring, .strikeline { position: absolute; z-index: 20; }
      .kw {
        padding: 22px 44px 30px;
        text-align: center;
        font-style: italic;
        font-weight: 700;
        font-size: 84px;
        line-height: 1.05;
        color: #1a1410;
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 300% auto;
        clip-path: polygon(0% 8%, 10% 0%, 35% 5%, 60% 0%, 85% 6%, 100% 2%, 99% 50%, 100% 94%, 80% 100%, 55% 95%, 30% 100%, 8% 96%, 0% 100%, 1.5% 50%);
        filter: drop-shadow(0 14px 18px rgba(26, 20, 16, 0.5));
      }
      .kw span { display: block; white-space: nowrap; }
      .kw.dark { color: #efe3c8; background: #1a1410 url("assets/decors/parchemin.jpg") center / 300% auto; background-blend-mode: multiply; }
      .kw.red { color: #8b2e1f; }
      .kw.gold { color: #8b2e1f; background-color: #f6d77f; background-blend-mode: multiply; }
      .kw.small { font-size: 58px; padding: 16px 34px 22px; }
      .kw small {
        display: block;
        font-family: "EB Garamond", Georgia, serif;
        font-style: normal;
        font-weight: 500;
        font-size: 28px;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: #8b5e34;
        margin-top: 6px;
      }
      .hero {
        left: 0;
        width: 1080px;
        text-align: center;
        font-weight: 700;
        font-size: 190px;
        line-height: 0.95;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #f6d77f;
        -webkit-text-stroke: 16px #1a1410;
        paint-order: stroke fill;
        filter: drop-shadow(0 14px 20px rgba(0, 0, 0, 0.6));
      }
      .hero span { display: block; }
      .hero.rust { color: #c9482b; }
      .hero.cream { color: #f4ead2; }
      .refchip {
        padding: 10px 30px 14px;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 34px;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: #efe3c8;
        background: rgba(26, 20, 16, 0.86);
        border: 3px solid #c8963e;
      }
      .refchip span { display: block; white-space: nowrap; }
      .ring { overflow: visible; pointer-events: none; z-index: 15; }
      .ring circle { fill: none; stroke-width: 12; stroke-dasharray: 1000; stroke-linecap: round; filter: drop-shadow(0 0 10px rgba(246, 215, 127, 0.9)); }
      .strikeline { left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; z-index: 25; }

      /* ---------- captions ---------- */
      .cap {
        position: absolute;
        left: 50px;
        top: 1215px;
        width: 840px;
        margin: 0;
        text-align: center;
        font-weight: 700;
        font-size: 72px;
        line-height: 1.1;
        color: #f4ead2;
        z-index: 60;
      }
      .capin {
        display: inline-block;
        padding: 12px 34px 20px;
        background: rgba(26, 20, 16, 0.86);
        border-radius: 16px;
        border-bottom: 5px solid #c8963e;
        box-shadow: 0 12px 26px rgba(0, 0, 0, 0.45);
      }
      .cw { display: inline-block; margin: 0 0.05em; }

      /* ---------- global overlays ---------- */
      #progress { position: absolute; left: 0; top: 0; width: 1080px; height: 10px; z-index: 95; background: rgba(26, 20, 16, 0.5); }
      #progress i { display: block; width: 100%; height: 100%; background: #f6d77f; transform-origin: 0 50%; }
      #flash { position: absolute; inset: 0; z-index: 90; opacity: 0; pointer-events: none; background: #f6d77f; }

      .mote { position: absolute; border-radius: 50%; background: #f6d77f; box-shadow: 0 0 8px rgba(246, 215, 127, 0.85); }
      #motes { position: absolute; inset: 0; z-index: 50; pointer-events: none; }

      @keyframes hf-grain-noise {
        0%, 100% { transform: translate(0, 0); }
        10% { transform: translate(-5%, -5%); }
        20% { transform: translate(-10%, 5%); }
        30% { transform: translate(5%, -10%); }
        40% { transform: translate(-5%, 15%); }
        50% { transform: translate(-10%, 5%); }
        60% { transform: translate(15%, 0); }
        70% { transform: translate(0, 10%); }
        80% { transform: translate(-15%, 0); }
        90% { transform: translate(10%, 5%); }
      }
      #grain-overlay .grain-texture {
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
        opacity: 0.11;
        animation: hf-grain-noise 0.5s steps(1) infinite;
      }

      /* ---------- project-specific pieces ---------- */
      .portrait {
        position: absolute;
        overflow: hidden;
        border: 6px solid #c8963e;
        box-shadow: 0 16px 26px rgba(26, 20, 16, 0.5);
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 260% auto;
      }
      .portrait img { position: absolute; }
      .half { position: absolute; top: 0; height: 1920px; overflow: hidden; }
      .half img { position: absolute; }
      .divider { position: absolute; left: 538px; top: 0; width: 4px; height: 1920px; background: #f6d77f; transform-origin: 50% 0; z-index: 12; }

      .medallion { position: absolute; width: 500px; height: 500px; filter: drop-shadow(0 18px 26px rgba(26, 20, 16, 0.55)); z-index: 20; }
      .medallion .disc {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 260% auto;
        box-shadow: inset 0 0 60px rgba(139, 94, 52, 0.45);
      }
      .medallion svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
      .medallion circle { fill: none; stroke: #c8963e; stroke-width: 6; stroke-dasharray: 1500; }
      .medallion .inner { stroke: #8b5e34; stroke-width: 2; stroke-dasharray: 1300; }
      .medal-num {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 268px;
        line-height: 1;
        padding-bottom: 30px;
        box-sizing: border-box;
        color: #8b2e1f;
        -webkit-text-stroke: 5px #f6d77f;
        paint-order: stroke fill;
      }

      .tiles { position: absolute; left: 0; width: 1080px; height: 300px; z-index: 18; }
      .tile {
        position: absolute;
        top: 0;
        width: 200px;
        height: 260px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 400% auto;
        border: 3px solid #8b5e34;
        border-radius: 10px;
        box-shadow: 0 14px 22px rgba(26, 20, 16, 0.45);
      }
      .tile .val { font-family: "EB Garamond", Georgia, serif; font-weight: 700; font-size: 48px; color: #8b2e1f; line-height: 1; }
      .tile .heb { font-family: "Frank Ruhl Libre", serif; font-weight: 500; font-size: 150px; line-height: 1.05; color: #1a1410; }
      .tile.small { width: 118px; height: 230px; }
      .tile.small .val { font-size: 36px; }
      .tile.small .heb { font-size: 112px; }
      .hebword {
        position: absolute;
        left: 0;
        width: 1080px;
        margin: 0;
        text-align: center;
        font-family: "Frank Ruhl Libre", serif;
        font-weight: 700;
        font-size: 190px;
        line-height: 1;
        color: #1a1410;
        z-index: 18;
      }
      .total, .running {
        position: absolute;
        left: 0;
        width: 1080px;
        margin: 0;
        text-align: center;
        font-weight: 700;
        line-height: 1;
        color: #8b2e1f;
        z-index: 18;
      }
      .total { font-size: 250px; }
      .running { font-size: 170px; }
      .stamp {
        position: absolute;
        left: 200px;
        width: 680px;
        padding: 12px 0 18px;
        text-align: center;
        font-family: "EB Garamond", Georgia, serif;
        font-weight: 700;
        font-size: 96px;
        letter-spacing: 10px;
        text-transform: uppercase;
        color: #8b2e1f;
        border: 9px double #8b2e1f;
        background: rgba(239, 227, 200, 0.92);
        z-index: 22;
      }
      .cta {
        position: absolute;
        left: 90px;
        width: 740px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding: 20px 28px 24px;
        box-sizing: border-box;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 40px;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #1a1410;
        background: #f6d77f;
        border: 4px solid #1a1410;
        z-index: 30;
      }
      .bubble { width: 70px; height: 60px; overflow: visible; flex: none; }
      .bubble path { fill: none; stroke: #8b2e1f; stroke-width: 7; stroke-linejoin: round; stroke-dasharray: 420; }
      .head { position: absolute; left: 80px; width: 920px; text-align: center; z-index: 18; }
      .title { margin: 0 0 24px; font-weight: 700; font-size: 124px; line-height: 1.02; color: #1a1410; }
      .endkicker {
        display: block;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 36px;
        letter-spacing: 10px;
        text-transform: uppercase;
        color: #8b5e34;
        margin-bottom: 18px;
      }
      .endrule { display: block; width: 460px; height: 2px; margin: 0 auto 24px; background: #8b5e34; }
      .subpill {
        position: absolute;
        left: 190px;
        width: 700px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 24px;
        padding: 26px 30px 30px;
        box-sizing: border-box;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 58px;
        font-weight: 700;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: #efe3c8;
        background: #8b2e1f;
        border: 5px solid #1a1410;
        border-radius: 999px;
        box-shadow: 0 14px 26px rgba(26, 20, 16, 0.5);
        z-index: 30;
      }
      .subpill svg { width: 64px; height: 64px; flex: none; }
      .gold-glow {
        position: absolute;
        left: 0;
        top: 250px;
        width: 1080px;
        height: 1100px;
        background: radial-gradient(ellipse at 45% 50%, rgba(246, 215, 127, 0.55) 0%, rgba(246, 215, 127, 0) 62%);
        z-index: 3;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-width="1080"
      data-height="1920"
      data-duration="{{DURATION}}"
    >
      {{SCENES}}

      <div id="motes">{{MOTES}}</div>

      {{CAPTIONS}}

      <div id="progress"><i></i></div>
      <div id="flash"></div>

      <div id="grain-overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100">
        <div class="grain-texture"></div>
      </div>

      {{AUDIO}}
    </div>

    <script>
      const tl = gsap.timeline({ paused: true });
      {{TWEENS}}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
