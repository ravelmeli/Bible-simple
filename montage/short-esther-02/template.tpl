<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>La Bible Simple - Esther - style 02</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {
        font-family: "Inter";
        src: url("assets/fonts/Inter.ttf") format("truetype");
        font-weight: 100 900;
        font-style: normal;
      }
      html, body { margin: 0; background: #E9EDF1; }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        font-family: "Inter", sans-serif;
        color: #1B242E;
        background: #E9EDF1;
      }
      #darkbg { position: absolute; inset: 0; background: #1B242E; opacity: 0; }
      #drift { position: absolute; inset: 0; transform-origin: 50% 50%; }
      #world {
        position: absolute;
        left: 0;
        top: 0;
        width: {{WORLD_W}}px;
        height: {{WORLD_H}}px;
        transform-origin: 0 0;
        background-image: radial-gradient(circle, rgba(27, 36, 46, 0.16) 2px, transparent 2.6px);
        background-size: 40px 40px;
      }

      .node { position: absolute; }
      .sticker img { display: block; filter: drop-shadow(0 18px 22px rgba(27, 36, 46, 0.28)) drop-shadow(0 3px 4px rgba(27, 36, 46, 0.18)); }

      .headline .kick {
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 26px;
        font-weight: 600;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: #6B7785;
        margin-bottom: 22px;
      }
      .headline .kick i { display: block; width: 18px; height: 18px; background: #F85830; }
      .headline .h { font-weight: 800; line-height: 1.08; letter-spacing: -1.5px; }
      .headline .sub { margin-top: 18px; font-size: 30px; color: #6B7785; }
      .headline.dark { color: #E9EDF1; }
      .headline.dark .kick { color: #8A97A6; }
      .hl { position: relative; display: inline-block; font-style: normal; }
      .hl span { position: relative; z-index: 1; }
      .hl i {
        position: absolute;
        left: -4px;
        right: -4px;
        bottom: 0.06em;
        height: 0.26em;
        background: #F85830;
        transform-origin: 0 50%;
        z-index: 0;
      }

      .lead { pointer-events: none; overflow: visible; }
      .lead line, .lead path { stroke: #1B242E; stroke-width: 3; fill: none; }
      .lead circle { fill: #F85830; }
      .arrows path { stroke: #8A97A6; stroke-width: 6; stroke-linecap: round; }

      .label { padding-left: 18px; border-left: 4px solid #F85830; }
      .label.dark b { color: #E9EDF1; }
      .label.dark span { color: #8A97A6; }
      .label b { display: block; font-size: 36px; font-weight: 700; line-height: 1.15; white-space: nowrap; }
      .label span { display: block; margin-top: 6px; font-size: 24px; color: #6B7785; white-space: nowrap; }

      .tag {
        padding: 12px 24px 14px;
        font-weight: 800;
        line-height: 1.1;
        white-space: nowrap;
        color: #1B242E;
        background: #FFFFFF;
        border: 3px solid #1B242E;
        box-shadow: 6px 6px 0 rgba(27, 36, 46, 0.18);
      }
      .tag.acc { color: #FFFFFF; background: #F85830; border-color: #F85830; }
      .tag.dark { color: #E9EDF1; background: transparent; border-color: transparent; box-shadow: none; padding-left: 0; }
      .ref {
        padding: 6px 14px 8px;
        font-size: 24px;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #6B7785;
        border: 2px solid #AEB8C3;
        white-space: nowrap;
      }

      .grid { display: grid; grid-template-columns: repeat(12, 38px); gap: 6px; }
      .grid i { display: block; width: 38px; height: 38px; border-radius: 4px; background: #CBD3DC; }
      .counter { font-weight: 800; letter-spacing: -2px; line-height: 1; color: #F85830; white-space: nowrap; }
      .counter .unit { font-size: 0.42em; letter-spacing: 0; margin-left: 6px; color: #1B242E; font-weight: 700; }
      .counter.dark .unit { color: #E9EDF1; }

      .box {
        width: 500px;
        padding: 26px 30px 30px;
        box-sizing: border-box;
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        line-height: 1.2;
        background: #FFFFFF;
        border: 3px solid #1B242E;
        box-shadow: 8px 8px 0 rgba(27, 36, 46, 0.15);
      }
      .box.q { width: 620px; border-radius: 26px; }
      .box.out { width: 300px; font-size: 64px; font-weight: 800; }
      .box small { display: block; font-size: 24px; font-weight: 600; letter-spacing: 4px; text-transform: uppercase; color: #6B7785; margin-bottom: 4px; }
      .box.out small { color: inherit; opacity: 0.8; }

      .day {
        width: 280px;
        padding: 28px 0 34px;
        text-align: center;
        font-size: 150px;
        font-weight: 800;
        line-height: 1;
        border: 3px solid #1B242E;
        box-shadow: 8px 8px 0 rgba(27, 36, 46, 0.15);
      }
      .day.wide { width: 300px; font-size: 64px; padding: 26px 0 30px; }
      .day small { display: block; font-size: 26px; font-weight: 600; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 10px; opacity: 0.85; }
      .dot { width: 30px; height: 30px; border-radius: 50%; background: #F85830; }
      .bar { background: #1B242E; }
      .bar.acc { background: #F85830; }
      .zero { font-size: 400px; font-weight: 900; line-height: 0.9; color: #F85830; letter-spacing: -10px; }
      .cta {
        display: flex;
        align-items: center;
        gap: 22px;
        padding: 22px 34px 26px;
        font-size: 44px;
        font-weight: 700;
        color: #1B242E;
        background: #FFFFFF;
        white-space: nowrap;
      }
      .cta svg { width: 70px; height: 60px; }
      .cta path { fill: none; stroke: #F85830; stroke-width: 9; stroke-linejoin: round; }

      .map { display: block; overflow: hidden; }
      .map .land { fill: #D3DAE2; stroke: #AEB8C3; stroke-width: 1.5; }
      .map .empire { fill: rgba(248, 88, 48, 0.16); stroke: #F85830; stroke-width: 4; stroke-dasharray: 3000; stroke-linejoin: round; }
      .map .pdot { fill: #F85830; }
      .map .place circle { fill: #1B242E; stroke: #FFFFFF; stroke-width: 4; }
      .map .place text { font-family: "Inter", sans-serif; font-size: 34px; font-weight: 700; fill: #1B242E; paint-order: stroke; stroke: #E9EDF1; stroke-width: 8px; }
      .mapwrap { padding: 14px; background: #FFFFFF; border: 3px solid #1B242E; box-shadow: 8px 8px 0 rgba(27, 36, 46, 0.15); }
      .route { pointer-events: none; overflow: visible; }
      .route line { stroke: #F85830; stroke-width: 10; stroke-linecap: round; fill: none; }
      .route circle { fill: #F85830; }
      #grain {
        position: absolute;
        inset: -50%;
        z-index: 65;
        pointer-events: none;
        opacity: 0.05;
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        animation: hf-grain 0.5s steps(1) infinite;
      }
      @keyframes hf-grain {
        0%, 100% { transform: translate(0, 0); }
        25% { transform: translate(-4%, 3%); }
        50% { transform: translate(3%, -4%); }
        75% { transform: translate(-3%, -2%); }
      }
      #endcard .es { position: absolute; filter: drop-shadow(0 18px 22px rgba(0, 0, 0, 0.45)); }

      /* ---- screen-fixed chrome ---- */
      #chrome { position: absolute; left: 70px; top: 160px; width: 870px; z-index: 50; color: #1B242E; }
      #brand { display: flex; align-items: center; gap: 12px; font-size: 24px; font-weight: 800; letter-spacing: 4px; text-transform: uppercase; }
      #brand i { display: block; width: 16px; height: 16px; background: #F85830; }
      #chapters { display: flex; gap: 16px; margin-top: 16px; }
      .ch { position: relative; flex: 1; padding-bottom: 10px; font-size: 20px; font-weight: 600; white-space: nowrap; }
      .ch b { font-weight: 800; color: inherit; }
      .ch::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 3px; background: currentColor; opacity: 0.18; }
      .ch i { position: absolute; left: 0; right: 0; bottom: 0; height: 3px; background: #F85830; transform-origin: 0 50%; }

      .cap {
        position: absolute;
        left: 60px;
        top: 1440px;
        width: 820px;
        margin: 0;
        text-align: center;
        font-weight: 700;
        font-size: 56px;
        line-height: 1.15;
        z-index: 60;
      }
      .capin {
        display: inline-block;
        padding: 12px 30px 16px;
        color: #1B242E;
        background: #FFFFFF;
        border: 3px solid #1B242E;
        box-shadow: 6px 6px 0 rgba(27, 36, 46, 0.2);
      }
      .cw { display: inline-block; }

      #endcard {
        position: absolute;
        inset: 0;
        z-index: 70;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #1B242E;
        opacity: 0;
      }
      #endcard .kick { font-size: 28px; font-weight: 600; letter-spacing: 8px; text-transform: uppercase; color: #8A97A6; margin-bottom: 26px; }
      #endcard .h { font-size: 132px; font-weight: 900; line-height: 1; letter-spacing: -3px; color: #E9EDF1; text-align: center; }
      #endcard .sub2 {
        margin-top: 70px;
        padding: 24px 56px 28px;
        font-size: 52px;
        font-weight: 800;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #FFFFFF;
        background: #F85830;
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{{DURATION}}">
      <div id="darkbg"></div>
      <div id="drift">
        <div id="world">
        {{WORLD}}
        </div>
      </div>

      <div id="chrome">
        <div id="brand"><i></i>La Bible Simple</div>
        <div id="chapters">{{CHAPTERS}}</div>
      </div>

      {{CAPTIONS}}

      <div id="endcard">
        <div class="kick">Abonne-toi</div>
        <div class="h">La Bible<br /><em class="hl"><span>Simple</span><i></i></em></div>
        <div class="sub2">S'abonner</div>
        <img class="es" id="es1" src="assets/stickers/tete-garde-perse.png" style="left:40px;top:1180px;width:380px;height:330px;transform:rotate(-6deg)" />
        <img class="es" id="es2" src="assets/stickers/esther-pied.png" style="left:790px;top:1060px;width:240px;height:477px;transform:rotate(5deg)" />
      </div>
      <div id="grain"></div>

      {{AUDIO}}
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      {{TWEENS}}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
