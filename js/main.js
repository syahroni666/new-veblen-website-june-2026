/* ════════════════════════════════════════════════════════════
   Veblen Group — Own The Market · v3 interaction layer
   The Journey: calm particle ocean → warp INTO the dots →
   inverted orange world → settle back out into the site.
   Plus: char-split hero, market-share HUD, horizontal case
   panels, poster drift, parallax numerals, magnetic CTAs.
   Canvas 3D projection only — no WebGL library. ~50KB gz total.
   ════════════════════════════════════════════════════════════ */

(function () {
  "use strict";

  var staticMode = /[?&]static=1/.test(location.search); // QA mode: no animation, all content visible
  if (staticMode) document.documentElement.classList.add("static");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches || staticMode;
  var isMobile = window.matchMedia("(max-width: 760px)").matches;

  /* ── nav ── */
  var nav = document.getElementById("nav");
  var onScrollNav = function () { nav.classList.toggle("is-scrolled", window.scrollY > 40); };
  window.addEventListener("scroll", onScrollNav, { passive: true });
  onScrollNav();

  /* intercept all internal anchor clicks so ScrollTrigger pin-spacers
     don't throw off the scroll destination, and offset for fixed navbar */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      if (!id || id === "#") return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      history.pushState(null, "", id);
      var navH = nav ? nav.getBoundingClientRect().height : 0;
      var absTop = 0, walker = target;
      while (walker) { absTop += walker.offsetTop; walker = walker.offsetParent; }
      window.scrollTo({ top: Math.max(0, absTop - navH - 8), behavior: "smooth" });
    });
  });

  /* ── hero headline char split ── */
  document.querySelectorAll("[data-split]").forEach(function (el) {
    var text = el.textContent;
    el.textContent = "";
    el.setAttribute("aria-hidden", "true");
    for (var i = 0; i < text.length; i++) {
      var s = document.createElement("span");
      s.className = "ch";
      s.textContent = text[i];
      el.appendChild(s);
    }
  });

  /* ════════════════════════════════════════════════════════
     PARTICLE WORLD — one canvas, three states blended:
       ocean  (rolling wave plane, tilted to camera)
       tunnel (dots wrapped around the flight axis)
       warp   (camera speed → streaks, dots respawn behind)
     plus:
       takeover (0..1) grey → orange flood
       invert   (0..1) world flips: orange bg, ink dots
     ════════════════════════════════════════════════════════ */
  function ParticleWorld(canvas, opts) {
    opts = opts || {};
    var ctx = canvas.getContext("2d");
    var DPR = Math.min(window.devicePixelRatio || 1, 1.75);
    var pts = [];
    var W = 0, H = 0, t = 0, running = false;
    var self = this;

    this.takeover = opts.takeover || 0;
    this.morph = 0;     // 0 ocean → 1 tunnel
    this.speed = 0;     // warp velocity
    this.invert = 0;    // 0 normal → 1 orange world

    var COUNT = isMobile ? 1100 : (opts.count || 3200);
    var FOV = 520, CAM_Y = -260, CAM_Z = -560, TILT = 0.42;
    var DEPTH = 3000;   // tunnel depth before respawn
    var camZ = 0;       // flight distance through the tunnel
    var mouse = { x: 0, y: 0 };

    function resize() {
      W = canvas.clientWidth; H = canvas.clientHeight;
      canvas.width = W * DPR; canvas.height = H * DPR;
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      build();
    }

    function build() {
      pts.length = 0;
      /* wide + deep enough that the field runs edge-to-edge to the horizon */
      var spanX = 7000, spanZ = 5200;
      var cols = Math.round(Math.sqrt(COUNT * spanX / spanZ));
      var rows = Math.max(2, Math.round(COUNT / cols));
      for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
          var x = (c / (cols - 1) - 0.5) * spanX;
          var z = (r / (rows - 1)) * spanZ + 60;
          var ang = Math.random() * 6.2832;
          var rad = 220 + Math.random() * 720;
          pts.push({
            x: x, z: z,
            // tunnel coords: ring around the flight axis, own depth slot
            ta: ang, tr: rad, tz: Math.random() * DEPTH,
            tw: 0.5 + Math.random(),             // twinkle factor
            order: Math.min(1, (Math.hypot(x * 0.55, z - 500) / 3400) + (Math.sin(x * 0.013) + Math.cos(z * 0.011)) * 0.04)
          });
        }
      }
    }

    function frame() {
      if (!running) return;
      t += reduceMotion ? 0 : 0.012;
      camZ += self.speed;

      var m = self.morph, v = self.invert;

      /* environment: normal = transparent over site ink;
         inverted = solid orange world */
      ctx.clearRect(0, 0, W, H);
      if (v > 0.003) {
        ctx.fillStyle = "rgba(255,128,0," + v.toFixed(3) + ")";
        ctx.fillRect(0, 0, W, H);
      }

      var cosT = Math.cos(TILT), sinT = Math.sin(TILT);
      var mx = mouse.x * 90, my = mouse.y * 50;
      var streak = Math.min(1, self.speed / 26);

      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];

        /* ocean position */
        var oy = Math.sin(p.x * 0.0021 + t) * 46
               + Math.cos(p.z * 0.0028 + t * 0.8) * 38
               + Math.sin((p.x + p.z) * 0.0011 + t * 0.45) * 26;
        var oRy = oy * cosT - p.z * sinT;
        var oRz = oy * sinT + p.z * cosT;

        /* tunnel position (flying: depth loops as camera advances) */
        var tz = ((p.tz - camZ) % DEPTH + DEPTH) % DEPTH + 40;
        var wob = Math.sin(t * 1.6 + p.ta * 3) * 24;
        var tx = Math.cos(p.ta) * (p.tr + wob);
        var ty = Math.sin(p.ta) * (p.tr + wob) * 0.62; // squashed = widescreen tunnel

        /* blend ocean → tunnel */
        var bx = p.x + (tx - p.x) * m;
        var by = oRy + (ty - CAM_Y - oRy) * m;   // tunnel centred on camera axis
        var bz = oRz + (tz - oRz) * m;

        var pz = bz - CAM_Z;
        if (pz < 50) continue;
        var scale = FOV / pz;
        var sx = W / 2 + (bx + mx) * scale;
        var sy = H * 0.46 + (by - CAM_Y + my * (1 - m * 0.5)) * scale;
        if (sx < -30 || sx > W + 30 || sy < -30 || sy > H + 30) continue;

        var owned = self.takeover >= p.order;
        var r = Math.max(0.55, (2.6 + m * 1.1) * scale);

        /* colour: grey → orange flood; inverted world flips to ink/cream */
        var fill;
        if (v > 0.5) {
          var lum = 0.55 + 0.45 * Math.sin(t * 3 * p.tw + p.ta * 5);
          fill = "rgba(10,9,8," + (0.5 + 0.5 * lum * Math.min(1, scale * 1.6)).toFixed(3) + ")";
        } else if (owned) {
          var age = Math.min((self.takeover - p.order) / 0.1, 1);
          fill = "rgba(255,128,0," + (0.3 + 0.7 * age * Math.min(1, scale * 1.6)).toFixed(3) + ")";
        } else {
          fill = "rgba(242,237,230," + (0.05 + 0.16 * Math.min(1, scale * 1.4)).toFixed(3) + ")";
        }

        if (streak > 0.05 && m > 0.4) {
          /* motion streaks: project the same dot slightly deeper */
          var pz2 = pz + 90 + 320 * streak;
          var s2 = FOV / pz2;
          ctx.strokeStyle = fill;
          ctx.lineWidth = Math.max(0.6, r * 0.9);
          ctx.beginPath();
          ctx.moveTo(sx, sy);
          ctx.lineTo(W / 2 + (bx + mx) * s2, H * 0.46 + (by - CAM_Y + my * (1 - m * 0.5)) * s2);
          ctx.stroke();
        } else {
          ctx.fillStyle = fill;
          ctx.beginPath();
          ctx.arc(sx, sy, r, 0, 6.2832);
          ctx.fill();
        }
      }
      requestAnimationFrame(frame);
    }

    this.start = function () { if (!running) { running = true; requestAnimationFrame(frame); } };
    this.stop = function () { running = false; };
    this.setMouse = function (x, y) { mouse.x = x; mouse.y = y; };

    window.addEventListener("resize", resize);
    resize();

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (e) {
        e[0].isIntersecting ? self.start() : self.stop();
      }).observe(canvas);
    } else { this.start(); }
  }

  var hero = new ParticleWorld(document.getElementById("market-grid"));
  var cta = null;

  /* ── TEXT DUST — Thanos-snap: glyph pixels → upward drift ── */
  var textDust = (function () {
    var dustCanvas = document.getElementById("text-dust");
    if (!dustCanvas || reduceMotion) return null;

    var dctx = dustCanvas.getContext("2d");
    var DDPR = Math.min(window.devicePixelRatio || 1, 1.75);
    var pts = [];
    var cPts = [];
    var built = false;
    var _titleEl   = document.querySelector(".hero__title");
    var _competeEl = document.querySelector(".hero__compete");

    function resizeDust() {
      dustCanvas.width  = dustCanvas.clientWidth  * DDPR;
      dustCanvas.height = dustCanvas.clientHeight * DDPR;
      dctx.setTransform(DDPR, 0, 0, DDPR, 0, 0);
    }

    /* Sample actual glyph pixels from an offscreen canvas.
       Falls back to random bounding-box fill if getImageData is blocked. */
    function sampleEl(el, orange, base, outPts, riseSign) {
      var r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      var text = el.textContent;
      var style = window.getComputedStyle(el);
      var fs  = parseFloat(style.fontSize);
      var fw  = style.fontWeight  || "900";
      var ff  = style.fontFamily  || "Lexend, sans-serif";
      var fst = style.fontStyle   || "normal";
      var isSerif = ff.indexOf("DM Serif") !== -1;

      var sc = 0.32; /* render at 32% size for perf */
      var W  = Math.max(4, Math.ceil(r.width  * sc));
      var H  = Math.max(4, Math.ceil(r.height * sc));
      var off = document.createElement("canvas");
      off.width = W; off.height = H;
      var oc = off.getContext("2d");
      oc.font          = fst + " " + fw + " " + (fs * sc) + "px " + ff;
      oc.fillStyle     = "#fff";
      oc.textBaseline  = "alphabetic";
      /* Compute baseline to match CSS line-box layout:
         CSS puts baseline at fontAscent + halfLeading, where
         halfLeading = (lineBoxH - fontNaturalH) / 2.
         fontBoundingBoxAscent/Descent give the same metrics the browser uses. */
      var tm = oc.measureText(text);
      var baseline_y;
      if (tm.fontBoundingBoxAscent && tm.fontBoundingBoxDescent) {
        var fontH    = tm.fontBoundingBoxAscent + tm.fontBoundingBoxDescent;
        baseline_y   = tm.fontBoundingBoxAscent + (H - fontH) / 2;
        /* clamp so glyph stays within the canvas */
        baseline_y   = Math.max(tm.actualBoundingBoxAscent + 1,
                       Math.min(H - (tm.actualBoundingBoxDescent || 1) - 1, baseline_y));
      } else {
        baseline_y   = H * (isSerif ? 0.72 : 0.82);
      }
      oc.fillText(text, 2, baseline_y);

      var data, usePixels = false;
      try {
        data = oc.getImageData(0, 0, W, H).data;
        usePixels = true;
      } catch (e) { /* cross-origin font guard — fall through to bbox */ }

      var step = 2; /* sample every 2nd pixel at the reduced scale */
      if (usePixels) {
        for (var py = 0; py < H; py += step) {
          for (var px = 0; px < W; px += step) {
            if (data[(py * W + px) * 4 + 3] < 45) continue;
            addPt(r.left - base.left + px / sc, r.top - base.top + py / sc, orange, base.width, outPts, riseSign);
          }
        }
      } else {
        /* bbox fallback: dense random fill */
        var n = Math.min(100, Math.max(8, Math.round(r.width * r.height / 300)));
        for (var i = 0; i < n; i++) {
          addPt(r.left - base.left + Math.random() * r.width,
                r.top  - base.top  + Math.random() * r.height, orange, base.width, outPts, riseSign);
        }
      }
    }

    function addPt(sx, sy, orange, totalW, outPts, riseSign) {
      var target = outPts || pts;
      var sign   = (riseSign !== undefined) ? riseSign : -1;
      var xNorm = Math.max(0, Math.min(1, sx / totalW));
      target.push({
        x: sx, y: sy, orange: orange,
        delay:   xNorm * 0.28 + Math.random() * 0.06, /* left→right wave */
        riseAmt: sign * (55 + Math.random() * 150),
        driftX:  (Math.random() - 0.38) * 70,          /* slight rightward bias */
        size:    0.9 + Math.random() * 1.9
      });
    }

    function buildDust() {
      pts = []; cPts = [];
      var base = dustCanvas.getBoundingClientRect();
      if (base.width < 10) return;
      document.querySelectorAll(".ht:not(.ht--accent) .ch").forEach(function (el) { sampleEl(el, false, base); });
      document.querySelectorAll(".ht--accent .ch").forEach(function (el)           { sampleEl(el, true,  base); });
      document.querySelectorAll(".hero__serif").forEach(function (el)              { sampleEl(el, false, base); });
      document.querySelectorAll(".dotpulse").forEach(function (el)                 { sampleEl(el, true,  base); });
      /* compete-line: sample per .ch span so letter-spacing is captured via getBoundingClientRect */
      document.querySelectorAll(".hc--main .ch").forEach(function (el) { sampleEl(el, false, base, cPts, 1); });
      document.querySelectorAll(".hc--em .ch").forEach(function (el)   { sampleEl(el, true,  base, cPts, 1); });
      built = pts.length > 0;
    }

    function renderDust(heroProgress) {
      /* Phase 1 — APPEAR [0.022 → 0.038]: title fades out as particles fade in (crossfade).
         Phase 2 — SCATTER [0.038 → 0.19]: wave of particles drifts upward & fades.
         Guard on `built`: GSAP pin-spacer init scrubs before particles are ready. */
      var appearEff  = Math.max(0, Math.min(1, (heroProgress - 0.022) / 0.016));
      var scatterEff = Math.max(0, Math.min(1, (heroProgress - 0.038) / 0.152));

      /* Crossfade: title opacity is inverse of appearEff — they track each other
         so there's always full brightness and never a dark flash between states. */
      if (_titleEl) {
        if (!built || heroProgress < 0.022) {
          _titleEl.style.opacity = "";
        } else {
          _titleEl.style.opacity = String((1 - appearEff).toFixed(3));
        }
      }

      /* Compete-line phases:
           Gather    0.62 → 0.80  particles rise from below into text positions
           Crossfade 0.80 → 0.85  particles fade OUT, text DOM fades IN (never both at 100%)
           Final out 0.87 → 0.92  everything gone before takeover line
         renderDust owns _competeEl opacity — no GSAP autoAlpha on this element. */
      /* gather 0.62→0.76. crossfade is driven by cGatherEff itself — fires the
         instant particles are in position, no extra scroll gap needed. */
      var cGatherEff = Math.max(0, Math.min(1, (heroProgress - 0.62) / 0.14));
      var cCrossRaw  = Math.max(0, Math.min(1, (cGatherEff - 0.88) / 0.12));
      /* smoothstep: slow-fast-slow S-curve so the crossfade feels organic */
      var cCrossFade = cCrossRaw * cCrossRaw * (3 - 2 * cCrossRaw);
      /* Guard on built — same reason as _titleEl: GSAP pin-spacer init scrubs
         heroTL.progress() to ~0.85 before particles are ready, which would make
         the text flash visible on hard refresh. */
      if (_competeEl) _competeEl.style.opacity = built ? String(cCrossFade.toFixed(3)) : "0";

      var W = dustCanvas.clientWidth, H = dustCanvas.clientHeight;
      dctx.clearRect(0, 0, W, H);
      if (!built || heroProgress < 0.022) return;

      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];

        var driftT, alpha;
        if (scatterEff <= 0) {
          alpha  = appearEff;
          driftT = 0;
        } else {
          var waveT  = Math.max(0, Math.min(1, (scatterEff - p.delay) / 0.65));
          var scAlpha = 1 - waveT * waveT;
          alpha  = Math.min(appearEff, scAlpha);
          driftT = waveT;
        }

        if (alpha < 0.012) continue;

        dctx.globalAlpha = alpha;
        dctx.fillStyle   = p.orange ? "rgb(255,128,0)" : "rgb(242,237,230)";
        dctx.beginPath();
        dctx.arc(
          p.x + p.driftX  * driftT,
          p.y + p.riseAmt * driftT,
          Math.max(0.4, p.size * (1 - driftT * 0.35)),
          0, 6.2832
        );
        dctx.fill();
      }

      /* Compete-line coalesce: reversed wave — particles start scattered below
         their rest positions and converge upward into the text shape.
         (1-cCrossFade) ensures particles fade out exactly as text fades in. */
      var cAlphaEff = Math.max(0, Math.min(1, (heroProgress - 0.62) / 0.03));
      for (var j = 0; j < cPts.length; j++) {
        var cp = cPts[j];
        var cWaveT   = Math.max(0, Math.min(1, (cGatherEff - cp.delay) / 0.65));
        var reverseT = 1 - cWaveT;   /* 1 = scattered below, 0 = at rest */
        var cAlpha   = cWaveT * cWaveT * cAlphaEff * (1 - cCrossFade);
        if (cAlpha < 0.012) continue;

        dctx.globalAlpha = cAlpha;
        dctx.fillStyle   = cp.orange ? "rgb(255,128,0)" : "rgb(242,237,230)";
        dctx.beginPath();
        dctx.arc(
          cp.x + cp.driftX  * reverseT,
          cp.y + cp.riseAmt * reverseT,
          Math.max(0.4, cp.size * (1 - reverseT * 0.35)),
          0, 6.2832
        );
        dctx.fill();
      }

      dctx.globalAlpha = 1;
    }

    /* Wait for hero load-in animation (~1.25 s) + font readiness before sampling */
    document.fonts.ready.then(function () {
      setTimeout(function () { resizeDust(); buildDust(); }, 1600);
    });
    window.addEventListener("resize", function () { resizeDust(); buildDust(); });

    return { render: renderDust };
  })();

  window.addEventListener("pointermove", function (e) {
    var nx = (e.clientX / window.innerWidth - 0.5) * 2;
    var ny = (e.clientY / window.innerHeight - 0.5) * 2;
    hero.setMouse(nx, ny);
    if (cta) cta.setMouse(nx, ny);
  }, { passive: true });

  /* ── Google reviews — the 16 real reviews from the live site ── */
  var REVIEWS = [
    ["Luke Muir", "2 months ago", "Veblen completely transformed our lead flow. We went from chasing cold enquiries to having jobs booked automatically before a competitor even sees the notification. The AI follow-up alone has paid for itself ten times over."],
    ["Josh Norris", "3 months ago", "600 leads a month at under $32 CPL. The team built out our entire CRM, automated follow-up sequences, and the ads keep getting sharper. NT Trailers has never had a pipeline this full. These guys deliver."],
    ["David A.", "1 month ago", "Missed call text-back was live within days of onboarding and we started converting jobs we used to lose. The team is responsive, proactive and actually understands the trades. Worth every dollar."],
    ["David — ADV+ Painting", "5 months ago", "We started with Veblen from basically zero online presence. Within months they had Google Ads running, automations built out, and missed calls converting to booked jobs. We went from $0 to $50k a month in revenue — the system they built is genuinely incredible."],
    ["Amanda A", "9 weeks ago", "I recently had the pleasure of working with Veblen Group, and I must say, their professionalism and communication are outstanding. Highly recommend them to anyone looking for a quality marketing partner."],
    ["Southport Tyres", "8 months ago", "Best in the Business! So happy with the quality of work these guys produce. The attention to detail and creativity they bring is unmatched. Would not hesitate to recommend Veblen to anyone."],
    ["Kyle Albert", "10 months ago", "Zac was extremely professional and made the whole video process easy, even though I was new to it. He explained everything clearly, made me feel comfortable, and the final product was absolutely incredible."],
    ["Jane Prichard", "10 months ago", "We worked with Veblen on a short video project for our farm and couldn't be happier with the outcome. Zac was incredibly talented and professional throughout. The final video captured everything we hoped for and more."],
    ["Jared Kalischer", "10 months ago", "Veblen is Next Level — Absolute Game Changers! If you're looking for elite-level marketing that actually delivers results, look no further. The team is world-class and the work they produce is genuinely exceptional."],
    ["Mike & Charli McFarlane", "10 months ago", "Veblen is the media partner you want in your corner. The quality of the work, the passion they bring, and the results they deliver are genuinely next level. We couldn't recommend them more highly."],
    ["Danny Kalischer", "11 months ago", "Number 1 marketing company. The photos and videos that are produced are another level — genuinely the best creative output I've seen from any agency. Veblen are in a class of their own."],
    ["Luke Vaughan", "11 months ago", "We use Veblen right across our Group of companies for all things marketing. I was initially so impressed with Zac and the team — their strategic thinking and quality of execution is unlike any other agency we've worked with."],
    ["James Yoo", "11 months ago", "We've had a fantastic experience working with Veblen Group. Their team is professional, creative, and genuinely invested in the success of our business. The results have been outstanding across every campaign."],
    ["Kento Ito", "11 months ago", "Working with Veblen has been nothing short of exceptional. I've collaborated with them multiple times and they consistently deliver outstanding results. A truly world-class creative and marketing team."],
    ["Tom Mac", "11 months ago", "I spoke with Veblen 12 months ago and they worked out a plan to grow my business through social media. Not only have they delivered on everything they promised, they've exceeded every single expectation. The Timber Gang is booming."],
    ["Bishoy Youssef", "11 months ago", "Probably one of the best media companies I've worked with. The Veblen team came in, understood our company and brand, and produced content that truly represents who we are. An absolute pleasure to work with across multiple ventures."]
  ];
  var AV_COLORS = ["#f44336", "#9c27b0", "#3f51b5", "#03a9f4", "#009688", "#4caf50", "#ff9800", "#795548", "#607d8b", "#e91e63"];
  var G_SVG = '<svg class="gcard__g" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.5 6.1 29.5 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.2-.1-2.3-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.5 6.1 29.5 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C36.9 39.2 44 34 44 24c0-1.2-.1-2.3-.4-3.5z"/></svg>';

  function gcard(r, i) {
    var words = r[0].replace(/[^A-Za-z &]/g, "").split(/[\s&]+/).filter(Boolean);
    var initials = (words[0] ? words[0][0] : "V") + (words[1] ? words[1][0] : "");
    return '<article class="gcard">' +
      '<div class="gcard__head">' +
      '<span class="gcard__avatar" style="background:' + AV_COLORS[i % AV_COLORS.length] + '">' + initials.toUpperCase() + "</span>" +
      '<span class="gcard__who"><span class="gcard__name">' + r[0] + '</span><span class="gcard__when">' + r[1] + "</span></span>" +
      G_SVG + "</div>" +
      '<p class="gcard__stars">★★★★★</p>' +
      '<p class="gcard__text">' + r[2] + "</p></article>";
  }
  var trackA = document.getElementById("grev-a");
  var trackB = document.getElementById("grev-b");
  if (trackA && trackB) {
    var rowA = REVIEWS.slice(0, 8).map(gcard).join("");
    var rowB = REVIEWS.slice(8).map(function (r, i) { return gcard(r, i + 8); }).join("");
    trackA.innerHTML = rowA + rowA;   // duplicated for the seamless loop
    trackB.innerHTML = rowB + rowB;
  }

  /* ── HUD ── */
  var hudNum = document.getElementById("hud-num");
  var hudBar = document.getElementById("hud-bar");
  function setHud(p) {
    var pct = Math.min(100, Math.max(0, p * 100));
    hudNum.textContent = (pct < 10 ? "0" : "") + pct.toFixed(1);
    hudBar.style.width = pct + "%";
  }

  /* ════════ GSAP choreography ════════ */
  if (window.gsap && window.ScrollTrigger && !reduceMotion) {
    gsap.registerPlugin(ScrollTrigger);

    /* hero load-in */
    gsap.from(".ht .ch", { yPercent: 110, duration: 1.1, stagger: 0.035, ease: "power4.out", delay: 0.15 });
    gsap.from(".hero__serif, .hero__eyebrow, .hero__sub, .hero__ctas, .hero__cue", {
      autoAlpha: 0, y: 24, duration: 1, stagger: 0.08, ease: "power3.out", delay: 0.5
    });
    gsap.to(".hud", { autoAlpha: 1, duration: 0.8, delay: 1 });

    /* headline never sits still: each letter floats on its own slow wave */
    gsap.to(".ht .ch", {
      y: function () { return gsap.utils.random(-9, 9); },
      duration: function () { return gsap.utils.random(1.8, 2.8); },
      repeat: -1, yoyo: true, repeatRefresh: true,
      ease: "sine.inOut", delay: 1.4,
      stagger: { each: 0.06, from: "random" }
    });

    /* the whole lockup tilts in 3D toward the cursor */
    if (!isMobile) {
      var titleEl = document.querySelector(".hero__title");
      var tiltX = gsap.quickTo(titleEl, "rotationY", { duration: 0.9, ease: "power2.out" });
      var tiltY = gsap.quickTo(titleEl, "rotationX", { duration: 0.9, ease: "power2.out" });
      window.addEventListener("pointermove", function (e) {
        tiltX((e.clientX / window.innerWidth - 0.5) * 10);
        tiltY((e.clientY / window.innerHeight - 0.5) * -7);
      }, { passive: true });
    }

    /* THE JOURNEY — pinned ~320% of viewport:
       act 1 (0–.20): ocean, headline exits, flood begins
       act 2 (.20–.42): accelerate INTO the dots, morph to tunnel
       act 3 (.42–.62): orange world — environment fully inverted, warp line
       act 4 (.62–.84): decelerate, world restores, flood completes
       act 5 (.84–1): settle, takeover message, unpin into the site   */
    var J = { morph: 0, speed: 0, invert: 0, flood: 0 };
    function applyJ() {
      hero.morph = J.morph;
      hero.speed = J.speed;
      hero.invert = J.invert;
      hero.takeover = J.flood;
      /* Use scrollTrigger.progress (actual scroll position = 0 at page load)
         NOT heroTL.progress() which returns a non-zero value during GSAP's
         pin-spacer init scrub, causing 100% to appear on hard refresh. */
      setHud(heroTL.scrollTrigger ? heroTL.scrollTrigger.progress : 0);
      if (textDust) textDust.render(heroTL.progress());
      var hudEl = document.getElementById('hud');
      if (hudEl) hudEl.classList.toggle('hud--invert', J.invert > 0.1);
    }
    var heroTL = gsap.timeline({
      scrollTrigger: {
        trigger: "#hero", start: "top top", end: "+=240%",
        scrub: 0.5, pin: true, anticipatePin: 1
      },
      defaults: { ease: "none", onUpdate: applyJ }
    });
    heroTL
      /* act 1 — leave the surface */
      .to(J, { flood: 0.18, duration: 0.20 }, 0)
      /* Target .hero__inner (the parent wrapper) rather than its individual
         children. The load-in gsap.from already touched the children so
         animating them again breaks scrub reversal. The wrapper was never
         animated — GSAP has a clean slate, opacity scrubs and reverses cleanly.
         The title is hidden/restored via inline style inside renderDust(). */
      .to(".hero__inner", { opacity: 0, duration: 0.22, ease: "power2.in" }, 0.04)
      .to(".hero__cue",   { opacity: 0, duration: 0.08, ease: "power1.in" }, 0.04)
      /* act 2 — dive into the dots */
      .to(J, { morph: 1, speed: 34, duration: 0.22, ease: "power2.in" }, 0.20)
      .to(".hero__vignette", { opacity: 0, duration: 0.15 }, 0.24)
      .to("#nav", { autoAlpha: 0, duration: 0.08 }, 0.30)
      /* act 3 — the orange world */
      .to(J, { invert: 1, duration: 0.10 }, 0.42)
      .to("#warp-line", { autoAlpha: 1, duration: 0.06 }, 0.45)
      .fromTo("#warp-line", { scale: 0.92 }, { scale: 1.04, duration: 0.17 }, 0.45)
      .to("#warp-line", { autoAlpha: 0, duration: 0.06 }, 0.58)
      .to(J, { invert: 0, duration: 0.10 }, 0.62)
      /* act 4 — come out the other side */
      .to(J, { speed: 0, morph: 0, flood: 1.05, duration: 0.22, ease: "power2.out" }, 0.62)
      .to(".hero__vignette", { opacity: 1, duration: 0.15 }, 0.70)
      .to("#nav", { autoAlpha: 1, duration: 0.08 }, 0.74)
      /* act 5 — the market is yours */
      .fromTo("#takeover-line", { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.10 }, 0.84)
      .to(J, { flood: 1.25, duration: 0.16 }, 0.84);

    /* strike-through on "activity." */
    ScrollTrigger.create({
      trigger: ".strike", start: "top 75%",
      onEnter: function () { document.querySelector(".strike").classList.add("is-struck"); }
    });

    /* generic reveals (qualify has its own dive choreography) */
    gsap.utils.toArray("[data-reveal]").forEach(function (el) {
      if (el.closest("#qualify")) return;
      gsap.from(el, {
        y: 34, autoAlpha: 0, duration: 1, ease: "power3.out",
        scrollTrigger: { trigger: el, start: "top 88%" }
      });
    });

    /* horizontal case panels */
    var track = document.getElementById("cases-track");
    var horiz = gsap.to(track, {
      x: function () { return -(track.scrollWidth - window.innerWidth); },
      ease: "none",
      scrollTrigger: {
        trigger: "#cases", start: "top top", end: function () { return "+=" + (track.scrollWidth - window.innerWidth); },
        scrub: 0.6, pin: true, anticipatePin: 1, invalidateOnRefresh: true
      }
    });

    /* each giant numeral flies AT you as its panel arrives */
    gsap.utils.toArray(".casepanel").forEach(function (panel) {
      var big = panel.querySelector(".casepanel__big");
      gsap.from(big, {
        scale: 0.5, autoAlpha: 0, transformOrigin: "left center", ease: "power2.out",
        scrollTrigger: { trigger: panel, containerAnimation: horiz, start: "left 75%", end: "left 25%", scrub: 0.4 }
      });
    });

    /* counters — panel 1 fires on vertical approach, panels 2+ fire on horizontal entry */
    gsap.utils.toArray(".casepanel").forEach(function (panel, i) {
      var countEl = panel.querySelector(".count");
      if (!countEl) return;
      var target = parseFloat(countEl.dataset.count);
      var obj = { v: 0 };
      var stConfig = i === 0
        ? { trigger: "#cases", start: "top 80%", once: true }
        : { trigger: panel, containerAnimation: horiz, start: "left 60%", once: true };
      ScrollTrigger.create(Object.assign(stConfig, {
        onEnter: function () {
          gsap.to(obj, { v: target, duration: 1.6, ease: "power2.out",
            onUpdate: function () { countEl.textContent = Math.round(obj.v); }
          });
        }
      }));
    });

    /* THE PORTAL + CORRIDOR — one continuous shot.
       "STOP" overlays the corridor; through the hole of the O you can
       already see the work floating. Scroll flies you through the O,
       and the camera carries straight on past the posters. */
    var cam = document.getElementById("corridor-cam");
    var stopSvg = document.getElementById("stopper-svg");
    if (cam && stopSvg) {
      var posters = gsap.utils.toArray(".corridor .poster");
      var STEP = isMobile ? 560 : 780;
      var seats = [[-26, -10, -2], [24, 9, 2], [-21, 13, 1], [27, -13, -2], [-29, 3, 2], [20, -7, -1], [-17, -15, 1], [25, 14, 0]];
      posters.forEach(function (po, i) {
        var s = seats[i % seats.length];
        gsap.set(po, { xPercent: -50, yPercent: -50, x: s[0] + "vw", y: s[1] + "vh", z: -i * STEP - 500, rotationZ: s[2] });
      });
      var corridorDepth = posters.length * STEP + 200;
      var camPos = { z: 0 };
      var corridorDone = false;
      var camUpdate = function () {
        gsap.set(cam, { z: camPos.z });
        if (corridorDone) return;
        for (var i = 0; i < posters.length; i++) {
          var zEff = camPos.z - (i * STEP + 500);
          gsap.set(posters[i], { opacity: 1, visibility: zEff > 890 ? "hidden" : "visible" });
          if (posters[i].style.filter) posters[i].style.filter = "";
        }
      };

      /* map the O-hole centre (706,284 in viewBox units) to on-screen px,
         accounting for xMidYMid slice cropping — exact at any window size */
      var stopOrigin = function () {
        var r = stopSvg.getBoundingClientRect();
        var s = Math.max(r.width / 1200, r.height / 600);
        var ox = 687 * (r.width / 1200);
        var oy = 306 * (r.height / 600);
        return ox.toFixed(1) + "px " + oy.toFixed(1) + "px";
      };

      var journey = gsap.timeline({
        scrollTrigger: {
          trigger: "#corridor", start: "top top",
          end: "+=" + (isMobile ? 340 : 440) + "%",
          scrub: 0.5, pin: true, anticipatePin: 0, invalidateOnRefresh: true,
          onLeave: function () {
            corridorDone = true;
            posters.forEach(function (p) { gsap.set(p, { visibility: "hidden" }); });
            gsap.set(stopSvg, { display: 'none' });
            gsap.set(cam, { z: 0 });
          },
          onEnterBack: function () {
            corridorDone = false;
            gsap.set(cam, { z: corridorDepth });
            gsap.set(stopSvg, { display: '' });
            camUpdate();
          }
        },
        defaults: { ease: "none" }
      });
      journey
        /* slow drift behind the O so the floating work is alive in the hole */
        .to(camPos, { z: 140, duration: 0.2, onUpdate: camUpdate }, 0)
        .to(".stopper__top, .stopper__bottom", { autoAlpha: 0, duration: 0.05 }, 0.05)
        /* fly through the hole of the O straight into the work */
        .to(stopSvg, {
          scale: 44,
          transformOrigin: function () { return stopOrigin(); },
          duration: 0.2, ease: "power2.in"
        }, 0.02)
        /* the camera keeps flying — past every poster to the end */
        .to(camPos, { z: corridorDepth, duration: 0.77, onUpdate: camUpdate }, 0.23);
    }

    /* THE CHOICE — fork sides collide into frame from opposite edges */
    gsap.from(".forkside--p", {
      xPercent: -36, autoAlpha: 0, ease: "power2.out",
      scrollTrigger: { trigger: "#fork .fork__split", start: "top 85%", end: "top 45%", scrub: 0.6 }
    });
    gsap.from(".forkside--s", {
      xPercent: 36, autoAlpha: 0, ease: "power2.out",
      scrollTrigger: { trigger: "#fork .fork__split", start: "top 85%", end: "top 45%", scrub: 0.6 }
    });

    /* WORLD FLIP — the cream Systems world wipes open over the dark site */
    gsap.fromTo("#systems",
      { clipPath: "inset(10% 7% 10% 7% round 28px)", scale: 0.965 },
      {
        clipPath: "inset(0% 0% 0% 0% round 0px)", scale: 1, ease: "none",
        scrollTrigger: { trigger: "#systems", start: "top 90%", end: "top 25%", scrub: 0.5 }
      });

    /* section headings get a gentle parallax against their body */
    gsap.utils.toArray(".verticals h2, .partnership h2, .systems h2, .creative__title").forEach(function (el) {
      gsap.fromTo(el, { y: 50 }, {
        y: -30, ease: "none",
        scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: 1 }
      });
    });

    /* footer mega parallax */
    gsap.from(".footer__mega", {
      yPercent: 40, ease: "none",
      scrollTrigger: { trigger: ".footer", start: "top bottom", end: "bottom bottom", scrub: 0.6 }
    });

    /* THE SECOND DIVE — one last plunge into the dots before the form.
       Short pinned warp: accelerate, orange flash, settle, form lands. */
    if (cta) {
      var D = { m: 0, s: 0, v: 0 };
      var applyD = function () { cta.morph = D.m; cta.speed = D.s; cta.invert = D.v; };
      var diveTL = gsap.timeline({
        scrollTrigger: { trigger: "#qualify", start: "top top", end: "+=140%", scrub: 0.5, pin: true, anticipatePin: 1 },
        defaults: { ease: "none", onUpdate: applyD }
      });
      diveTL
        .fromTo(".qualify__inner", { autoAlpha: 0 }, { autoAlpha: 0, duration: 0.3 }, 0)
        .to(D, { m: 1, s: 30, duration: 0.32, ease: "power2.in" }, 0)
        .to(D, { v: 0.9, duration: 0.08 }, 0.32)
        .to(D, { v: 0, duration: 0.1 }, 0.44)
        .to(D, { s: 3, m: 0.25, duration: 0.3, ease: "power2.out" }, 0.44)
        .fromTo(".qualify__inner", { autoAlpha: 0, scale: 0.93, y: 40 }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.5);
    }

    /* deep links: re-land on the anchor after pin spacers change the layout */
    window.addEventListener("load", function () {
      if (location.hash) {
        var el = document.querySelector(location.hash);
        if (el) { ScrollTrigger.refresh(); el.scrollIntoView(); }
      }
    });
  } else {
    /* no-motion fallback: everything visible, market owned, counters final */
    document.documentElement.classList.add("static"); // flat layout for corridor etc.
    hero.takeover = 1.25;
    setHud(1);
    document.getElementById("hud").style.opacity = 1;
    document.getElementById("takeover-line").style.opacity = 1;
    document.querySelectorAll(".count").forEach(function (el) { el.textContent = el.dataset.count; });
  }

  /* ── magnetic CTAs ── */
  if (!isMobile && !reduceMotion) {
    document.querySelectorAll("[data-magnetic]").forEach(function (btn) {
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width / 2);
        var dy = e.clientY - (r.top + r.height / 2);
        btn.style.transform = "translate(" + dx * 0.18 + "px," + dy * 0.3 + "px)";
      });
      btn.addEventListener("pointerleave", function () {
        btn.style.transform = "";
        btn.style.transition = "transform 0.5s cubic-bezier(0.22,1,0.36,1)";
      });
    });
  }

  /* ── poster videos: attach on load (IntersectionObserver unreliable inside preserve-3d) ── */
  document.querySelectorAll(".poster[data-video]").forEach(function (fig) {
    var src = fig.dataset.video;
    if (!src) return;
    var v = document.createElement("video");
    v.src = src; v.muted = true; v.loop = true; v.playsInline = true; v.autoplay = true;
    v.setAttribute("preload", "none");
    (fig.querySelector(".poster__frame") || fig).prepend(v);
  });


  





  /* ── phone grid: muted autoplay previews + tap-for-sound full play ── */
  (function () {
    var phones = document.querySelectorAll(".ph[data-preview]");
    if (!phones.length) return;

    function stopFull() {
      document.querySelectorAll(".ph.fullplay").forEach(function (p) {
        var v = p.querySelector("video");
        if (v) { v.pause(); v.remove(); }
        p.classList.remove("fullplay");
        startPreview(p);
      });
    }

    function startPreview(p) {
      if (p.classList.contains("fullplay") || p.querySelector("video")) return;
      var v = document.createElement("video");
      v.src = p.dataset.preview;
      v.muted = true; v.loop = true; v.playsInline = true; v.autoplay = true;
      v.setAttribute("preload", "auto");
      v.setAttribute("aria-hidden", "true");
      p.querySelector(".ph__screen").appendChild(v);
      p.classList.add("previewing");
    }

    if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { startPreview(e.target); io.unobserve(e.target); }
        });
      }, { rootMargin: "120px" });
      phones.forEach(function (p) { io.observe(p); });
    }

    var isTouch = window.matchMedia("(hover: none)").matches;

    /* update label to match actual interaction */
    if (!isTouch) {
      document.querySelectorAll(".ph__sound").forEach(function (el) {
        el.textContent = "🔊 Hover for sound";
      });
    }

    function playFull(p) {
      if (p.classList.contains("fullplay")) return;
      stopFull();
      var prev = p.querySelector("video");
      if (prev) prev.remove();
      p.classList.remove("previewing");
      var v = document.createElement("video");
      v.src = p.dataset.full;
      v.poster = p.dataset.poster;
      v.autoplay = true; v.playsInline = true; v.loop = true;
      if (isTouch) v.controls = true;
      p.querySelector(".ph__screen").appendChild(v);
      p.classList.add("fullplay");
    }

    phones.forEach(function (p) {
      if (isTouch) {
        /* touch: tap to play audio, tap again to stop */
        p.addEventListener("click", function () {
          if (p.classList.contains("fullplay")) { stopFull(); } else { playFull(p); }
        });
      } else {
        /* desktop: hover in = audio on, hover out = audio off */
        p.addEventListener("mouseenter", function () { playFull(p); });
        p.addEventListener("mouseleave", function () { stopFull(); });
      }
    });
  })();

  /* ── qualifier: live routing + submit ──
     ENDPOINT: set QFORM_ENDPOINT (n8n webhook) before launch.
     Until then submissions fall back to email so no lead is lost. */
  var QFORM_ENDPOINT = "https://veblen-platform-production.up.railway.app/api/webhooks/intake/website-contact-us";

  var form = document.getElementById("qform");
  var revenueSelect = document.getElementById("q-revenue");
  var routeLine = document.getElementById("q-route");
  var successLine = document.getElementById("q-success");
  var isPremium = function (v) { return v === "1m-3m" || v === "3m-10m" || v === "10m-plus"; };

  revenueSelect.addEventListener("change", function () {
    routeLine.textContent = isPremium(revenueSelect.value)
      ? "You qualify for The Partnership — applications reviewed personally."
      : "Veblen Systems is your lane — fixed price, built in days.";
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var raw = {};
    new FormData(form).forEach(function (v, k) { raw[k] = v; });
    var params = new URLSearchParams(location.search);
    var data = {
      email: (raw.email || "").trim(),
      firstName: (raw.first_name || "").trim(),
      lastName: (raw.last_name || "").trim(),
      phone: (raw.phone || "").trim(),
      company: (raw.business || "").trim(),
      annualRevenue: raw.revenue,
      monthlyAdSpend: raw.ad_spend,
      entryPath: "website-qualifier-" + (isPremium(raw.revenue) ? "partnership" : "systems"),
      landingPageUrl: location.href,
      utm_source: params.get("utm_source") || undefined,
      utm_medium: params.get("utm_medium") || undefined,
      utm_campaign: params.get("utm_campaign") || undefined,
      utm_content: params.get("utm_content") || undefined
    };

    var done = function () {
      form.querySelector(".qform__submit").hidden = true;
      successLine.hidden = false;
    };
    var mailFallback = function () {
      window.location.href = "mailto:admin@veblengroup.com.au?subject=Website%20enquiry%20(" +
        encodeURIComponent(data.business || "") + ")&body=" +
        encodeURIComponent(JSON.stringify(data, null, 2));
    };

    if (QFORM_ENDPOINT) {
      fetch(QFORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (r.ok) { done(); } else { mailFallback(); } })
        .catch(mailFallback);
    } else {
      mailFallback();
      done();
    }
  });

  /* ── Corridor ambient particles ── */
  (function () {
    var canvas = document.getElementById('corridor-particles');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var W = 1, H = 1;

    function resize() {
      W = canvas.width  = canvas.offsetWidth  || canvas.parentElement.offsetWidth;
      H = canvas.height = canvas.offsetHeight || canvas.parentElement.offsetHeight;
    }
    resize();
    new ResizeObserver(resize).observe(canvas);

    /* ── config ── */
    var FOC       = 900;   // focal length px (matches CSS perspective: 900px)
    var NEAR      = 120;   // closest z before particle wraps
    var FAR       = 3600;  // furthest z
    var FOCAL_Z   = 1100;  // sharpest depth plane
    var COUNT     = 90;

    /* ── particle pool ── */
    var pts = [];
    for (var i = 0; i < COUNT; i++) pts.push(spawn());

    function spawn() {
      return {
        x  : (Math.random() - 0.5) * 1800,
        y  : (Math.random() - 0.5) * 1100,
        z  : NEAR + Math.random() * (FAR - NEAR),
        vx : (Math.random() - 0.5) * 0.35,
        vy : (Math.random() - 0.5) * 0.25,
        r  : 0.7 + Math.random() * 2.2,
        ph : Math.random() * Math.PI * 2,
        sp : 0.00035 + Math.random() * 0.00025,
        og : Math.random() < 0.28,   /* 28% orange, 72% warm white */
      };
    }

    /* read corridor cam's live translateZ set by GSAP */
    var camEl = document.getElementById('corridor-cam');
    function getCamZ() {
      if (!camEl || !camEl.style.transform) return 0;
      try { return new DOMMatrix(camEl.style.transform).m43; } catch (e) { return 0; }
    }

    var rafId = null;

    function frame(ts) {
      rafId = requestAnimationFrame(frame);
      var t    = ts * 0.001;
      var camZ = getCamZ();   /* positive = camera flew this far into the tunnel */

      ctx.clearRect(0, 0, W, H);
      var cx = W * 0.5, cy = H * 0.5;

      /* sort far → near so nearer orbs paint on top */
      pts.sort(function (a, b) { return b.z - a.z; });

      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];

        /* gentle float */
        p.x += p.vx + Math.sin(t * p.sp * 900 + p.ph) * 0.20;
        p.y += p.vy + Math.cos(t * p.sp * 700 + p.ph * 1.6) * 0.13;
        if (p.x >  950) { p.x =  950; p.vx = -Math.abs(p.vx); }
        if (p.x < -950) { p.x = -950; p.vx =  Math.abs(p.vx); }
        if (p.y >  650) { p.y =  650; p.vy = -Math.abs(p.vy); }
        if (p.y < -650) { p.y = -650; p.vy =  Math.abs(p.vy); }

        /* effective depth: camera flying forward makes particles approach */
        var ez = p.z - camZ * 0.55;
        if (ez < NEAR) { ez += (FAR - NEAR); p.z += (FAR - NEAR); } /* wrap to back */
        if (ez > FAR)  { ez -= (FAR - NEAR); p.z -= (FAR - NEAR); }

        /* perspective projection */
        var sc = FOC / ez;
        var sx = cx + p.x * sc;
        var sy = cy + p.y * sc;
        var pr = p.r * sc;               /* projected radius */

        if (pr < 0.15 || pr > 55) continue;
        if (sx < -100 || sx > W + 100 || sy < -100 || sy > H + 100) continue;

        /* depth-of-field: how far from focal plane? */
        var dof     = Math.min(1, Math.abs(ez - FOCAL_Z) / FOCAL_Z);
        /* alpha: fades at far end + dissolves at near edge + dof dimming */
        var farFade  = Math.pow(Math.min(1, ez / (FAR * 0.75)), 1.4);
        var nearFade = Math.min(1, (ez - NEAR) / 250);
        var alpha    = (1 - dof * 0.62) * (1 - farFade * 0.82) * nearFade;
        alpha        = Math.max(0, Math.min(1, alpha)) * Math.min(1, sc * 2.8);
        if (alpha < 0.012) continue;

        /* glow radius expands when out of focus — DoF bokeh look */
        var gr  = pr * (1.9 + dof * 5.5);
        var rgb = p.og ? '255,128,0' : '238,226,210';

        var g = ctx.createRadialGradient(sx, sy, 0, sx, sy, gr);
        g.addColorStop(0,    'rgba(' + rgb + ',' + Math.min(1, alpha * 1.3) + ')');
        g.addColorStop(0.30, 'rgba(' + rgb + ',' + (alpha * 0.50) + ')');
        g.addColorStop(1,    'rgba(' + rgb + ',0)');

        ctx.beginPath();
        ctx.arc(sx, sy, gr, 0, Math.PI * 2);
        ctx.fillStyle = g;
        ctx.fill();
      }
    }

    /* only animate while corridor is visible */
    new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        if (!rafId) rafId = requestAnimationFrame(frame);
      } else {
        if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
      }
    }, { threshold: 0 }).observe(canvas);
  })();

  /* ── FAQ accordion (smooth pixel-height animation) ── */
  (function () {
    var items = document.querySelectorAll('.faq__item');
    if (!items.length) return;

    function openItem(item) {
      item.setAttribute('open', '');
      var body = item.querySelector('.faq__body');
      var h = body.scrollHeight;
      body.style.height = h + 'px';
      item.classList.add('is-open');
      body.addEventListener('transitionend', function handler(e) {
        if (e.propertyName !== 'height') return;
        body.removeEventListener('transitionend', handler);
        body.style.height = 'auto';
      });
    }

    function closeItem(item) {
      var body = item.querySelector('.faq__body');
      body.style.height = body.scrollHeight + 'px';
      void body.offsetHeight; // commit height before animating to 0
      item.classList.remove('is-open');
      body.style.height = '0';
      body.addEventListener('transitionend', function handler(e) {
        if (e.propertyName !== 'height') return;
        body.removeEventListener('transitionend', handler);
        item.removeAttribute('open');
      });
    }

    items.forEach(function (item) {
      item.querySelector('summary').addEventListener('click', function (e) {
        e.preventDefault();
        var isOpen = item.classList.contains('is-open');
        items.forEach(function (other) {
          if (other !== item && other.classList.contains('is-open')) closeItem(other);
        });
        if (isOpen) { closeItem(item); } else { openItem(item); }
      });
    });
  })();

  /* ── services accordion ── */
  (function () {
    var items = document.querySelectorAll('.svc-item');
    if (!items.length) return;
    items.forEach(function (item) {
      var btn = item.querySelector('.svc-row');
      var body = item.querySelector('.svc-body');
      btn.addEventListener('click', function () {
        var isOpen = item.classList.contains('is-open');
        items.forEach(function (el) {
          el.classList.remove('is-open');
          el.querySelector('.svc-row').setAttribute('aria-expanded', 'false');
          el.querySelector('.svc-body').setAttribute('aria-hidden', 'true');
        });
        if (!isOpen) {
          item.classList.add('is-open');
          btn.setAttribute('aria-expanded', 'true');
          body.setAttribute('aria-hidden', 'false');
        }
      });
    });
  })();

})();
