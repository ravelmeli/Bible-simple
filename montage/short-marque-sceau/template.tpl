<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>La Bible Simple - Marque et sceau</title>
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

      .sc-in { position: absolute; inset: 0; }
      .bgset { position: absolute; inset: 0; overflow: hidden; }
      .bgimg, .paper {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .bgimg { filter: sepia(0.35) saturate(1.15) contrast(1.06) brightness(1.02); }
      .paper { mix-blend-mode: multiply; opacity: 0.5; }
      .vignette {
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 85% 70% at 50% 45%, rgba(26, 20, 16, 0) 55%, rgba(26, 20, 16, 0.6) 100%);
      }

      .el {
        position: absolute;
        filter: drop-shadow(16px 24px 24px rgba(26, 20, 16, 0.55)) sepia(0.12);
      }

      .card-wrap {
        position: absolute;
        filter: drop-shadow(0 22px 30px rgba(26, 20, 16, 0.55));
      }
      .card {
        position: relative;
        padding: 56px 66px 62px;
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 140% auto;
        clip-path: polygon(0% 3%, 6% 0%, 14% 2%, 27% 0%, 41% 2.5%, 55% 0.5%, 68% 2%, 82% 0%, 93% 2%, 100% 0.5%,
          99% 22%, 100% 45%, 98.5% 70%, 100% 97%, 91% 100%, 78% 98%, 63% 100%, 49% 98.5%, 34% 100%, 20% 98%, 7% 100%, 0% 97.5%,
          1% 72%, 0% 48%, 1.5% 24%);
        text-align: center;
      }
      .kicker {
        display: block;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 30px;
        letter-spacing: 8px;
        text-transform: uppercase;
        color: #8b5e34;
        margin-bottom: 16px;
      }
      .rule {
        display: block;
        width: 460px;
        height: 2px;
        margin: 0 auto 24px;
        background: #8b5e34;
      }
      .big { margin: 0; font-size: 80px; font-weight: 600; line-height: 1.08; }
      .p1-hook .big { font-size: 92px; }
      .mid { margin: 0; font-size: 62px; font-weight: 500; line-height: 1.14; }
      .small { margin: 0; font-size: 46px; font-weight: 500; line-height: 1.16; }
      .w { display: inline-block; }
      .accent { color: #8b2e1f; font-style: italic; }
      .ink { color: #1a1410; }
      .smallcaps { font-size: 0.55em; letter-spacing: 3px; color: #8b5e34; }

      .quote { margin: 0; font-style: italic; font-size: 64px; font-weight: 500; line-height: 1.14; }
      .ref {
        display: block;
        margin-top: 22px;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 28px;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: #8b5e34;
      }

      .ribbon {
        position: absolute;
        left: 80px;
        width: 920px;
        margin: 0;
        padding: 30px 40px 34px;
        box-sizing: border-box;
        text-align: center;
        font-style: italic;
        font-weight: 500;
        font-size: 66px;
        line-height: 1.15;
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 160% auto;
        clip-path: polygon(0% 6%, 8% 0%, 22% 4%, 39% 0%, 57% 5%, 74% 0%, 90% 4%, 100% 1%,
          99% 50%, 100% 95%, 86% 100%, 68% 96%, 50% 100%, 31% 96%, 14% 100%, 0% 95%, 1.5% 50%);
      }

      .medallion {
        position: absolute;
        width: 500px;
        height: 500px;
        filter: drop-shadow(0 18px 26px rgba(26, 20, 16, 0.55));
      }
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

      .tiles { position: absolute; left: 0; width: 1080px; height: 300px; }
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
      .tile .val {
        font-family: "EB Garamond", Georgia, serif;
        font-weight: 700;
        font-size: 48px;
        color: #8b2e1f;
        line-height: 1;
      }
      .tile .heb {
        font-family: "Frank Ruhl Libre", serif;
        font-weight: 500;
        font-size: 150px;
        line-height: 1.05;
        color: #1a1410;
      }
      .tile.small { width: 118px; height: 230px; }
      .tile.small .val { font-size: 36px; }
      .tile.small .heb { font-size: 112px; }

      .head { position: absolute; left: 80px; width: 920px; text-align: center; }
      .sum {
        position: absolute;
        left: 60px;
        width: 960px;
        margin: 0;
        text-align: center;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 50px;
        color: #1a1410;
      }
      .total {
        position: absolute;
        left: 0;
        width: 1080px;
        margin: 0;
        text-align: center;
        font-weight: 700;
        font-size: 230px;
        line-height: 1;
        color: #8b2e1f;
      }

      .stamp {
        position: absolute;
        left: 230px;
        width: 620px;
        padding: 12px 0 18px;
        text-align: center;
        font-family: "EB Garamond", Georgia, serif;
        font-weight: 700;
        font-size: 88px;
        letter-spacing: 10px;
        text-transform: uppercase;
        color: #8b2e1f;
        border: 9px double #8b2e1f;
        background: rgba(239, 227, 200, 0.9);
      }

      .cta {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 18px;
        margin-top: 30px;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 36px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #8b5e34;
      }
      .bubble { width: 66px; height: 56px; overflow: visible; }
      .bubble path { fill: none; stroke: #8b2e1f; stroke-width: 6; stroke-linejoin: round; stroke-dasharray: 420; }

      .title { margin: 0 0 24px; font-weight: 700; font-size: 124px; line-height: 1.02; }

      .portrait {
        position: absolute;
        width: 380px;
        height: 380px;
        border-radius: 50%;
        overflow: hidden;
        border: 6px solid #c8963e;
        box-shadow: 0 16px 26px rgba(26, 20, 16, 0.5);
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 260% auto;
      }
      .portrait img { position: absolute; }
      .plabel {
        position: absolute;
        width: 440px;
        margin: 0;
        text-align: center;
        font-family: "EB Garamond", Georgia, serif;
        font-size: 28px;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: #8b5e34;
      }
      .plabel b {
        display: block;
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 58px;
        letter-spacing: 0;
        text-transform: none;
        color: #1a1410;
      }
      .tag {
        position: absolute;
        margin: 0;
        padding: 18px 30px 22px;
        font-style: italic;
        font-weight: 600;
        font-size: 48px;
        line-height: 1.1;
        color: #1a1410;
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 300% auto;
        clip-path: polygon(0% 8%, 10% 0%, 35% 5%, 60% 0%, 85% 6%, 100% 2%, 99% 50%, 100% 94%, 80% 100%, 55% 95%, 30% 100%, 8% 96%, 0% 100%, 1.5% 50%);
      }
      .arrows { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
      .arrows path { fill: none; stroke: #8b2e1f; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 900; }
      .strike { position: relative; display: inline-block; }
      .strike i {
        position: absolute;
        left: -6px;
        right: -6px;
        top: 52%;
        height: 5px;
        background: #8b2e1f;
        transform-origin: 0 50%;
      }
      .gold-glow {
        position: absolute;
        left: 0;
        top: 300px;
        width: 1080px;
        height: 1100px;
        background: radial-gradient(ellipse at 45% 50%, rgba(246, 215, 127, 0.5) 0%, rgba(246, 215, 127, 0) 62%);
      }
      .cap {
        position: absolute;
        left: 80px;
        top: 1460px;
        width: 840px;
        margin: 0;
        padding: 18px 28px 22px;
        box-sizing: border-box;
        text-align: center;
        font-weight: 600;
        font-size: 50px;
        line-height: 1.15;
        color: #1a1410;
        background: #efe3c8 url("assets/decors/parchemin.jpg") center / 220% auto;
        clip-path: polygon(0% 8%, 9% 0%, 30% 5%, 52% 0%, 75% 5%, 92% 0%, 100% 6%, 99% 50%, 100% 93%, 88% 100%, 64% 95%, 40% 100%, 17% 96%, 0% 100%, 1% 50%);
        z-index: 60;
      }
      .cap .cw { display: inline-block; }

      .mote { position: absolute; border-radius: 50%; background: #f6d77f; filter: blur(1px); }
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
        opacity: 0.12;
        animation: hf-grain-noise 0.5s steps(1) infinite;
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
      data-duration="54"
    >
      {{SCENES}}

      <div id="motes">{{MOTES}}</div>

      <div id="grain-overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100">
        <div class="grain-texture"></div>
      </div>

      {{CAPTIONS}}

      {{AUDIO}}
    </div>

    <script>
      const tl = gsap.timeline({ paused: true });
      {{TWEENS}}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
