# -*- coding: utf-8 -*-
"""World-class testimonial presentation: featured cinema stage + filmstrip rail,
moved directly under the hero. Replaces the flat 7-tile wall."""
import re

BASE = "https://media.veblengroup.com.au/site/testimonials"

# slug, name, short, company, metric, metric label, quote (real Google-review lines only)
PEOPLE = [
    ("josh-nt-trailers", "Josh Norris", "Josh", "NT Trailers · Trailer Manufacturing", "600",
     "leads a month at under $32 CPL",
     "NT Trailers has never had a pipeline this full. These guys deliver."),
    ("luke-lcmb", "Luke Muir", "Luke", "LCMB Group · Electrical &amp; Air Conditioning", "100+",
     "qualified leads, every single month",
     "Jobs booked automatically before a competitor even sees the notification."),
    ("david-adv-painting", "David", "David", "ADV+ Painting · Trades", "$0→$50k",
     "monthly revenue, from zero online presence",
     "The system they built is genuinely incredible."),
    ("streamline-plumbing", "Streamline Plumbing", "Streamline", "Streamline Plumbing · Trades", "", "", ""),
    ("ardy-crown-realty", "Ardy", "Ardy", "Crown Realty · Real Estate", "", "", ""),
    ("kento-crown-realty", "Kento", "Kento", "Crown Realty · Real Estate", "", "", ""),
    ("bish-talentport", "Bishoy", "Bishoy", "TalentPort · Talent Placement", "", "", ""),
]

def thumb(i, p):
    slug, name, short, co, metric, mlabel, quote = p
    active = " is-active" if i == 0 else ""
    return ('        <button class="cine__thumb%s" type="button" role="tab" aria-label="Watch %s"\n'
            '          data-mp4="%s/%s.mp4" data-jpg="%s/%s.jpg" data-metric="%s" data-mlabel="%s" data-quote="%s" data-name="%s" data-co="%s">\n'
            '          <img src="%s/%s.jpg" alt="%s" loading="lazy" decoding="async" />\n'
            '          <span>%s</span>\n'
            '        </button>') % (active, name, BASE, slug, BASE, slug, metric, mlabel,
                                    quote.replace('"', "&quot;"), name, co, BASE, slug, name, short)

first = PEOPLE[0]
SECTION = '''<section class="films" id="films">
      <p class="secnum" data-reveal>01 — Proof, on camera</p>
      <h2 data-reveal>Hear it from <em class="serif">them.</em></h2>
      <p class="sub" data-reveal>Real owners, on camera, talking about what actually changed. No scripts, no actors.</p>

      <div class="cine" data-reveal>
        <div class="cine__stage">
          <div class="cine__framewrap">
            <div class="cine__glow" aria-hidden="true"></div>
            <div class="cine__frame" id="cine-frame">
              <img id="cine-poster" src="''' + BASE + '/' + first[0] + '''.jpg" alt="''' + first[1] + ''' testimonial" decoding="async" />
              <button class="cine__play" id="cine-play" type="button" aria-label="Play testimonial">
                <span class="cine__playring" aria-hidden="true"></span>
                <span class="cine__playicon">▶</span>
              </button>
            </div>
          </div>
          <div class="cine__meta">
            <p class="cine__metric" id="cine-metric">''' + first[4] + '''</p>
            <p class="cine__mlabel" id="cine-mlabel">''' + first[5] + '''</p>
            <p class="cine__quote" id="cine-quote">&ldquo;''' + first[6] + '''&rdquo;</p>
            <div class="cine__who">
              <p><strong id="cine-name">''' + first[1] + '''</strong><span id="cine-co">''' + first[3] + '''</span></p>
            </div>
            <p class="cine__veri"><span class="cine__stars">★★★★★</span> 5.0 · 16 Google reviews · all real clients</p>
          </div>
        </div>
        <div class="cine__rail" id="cine-rail" role="tablist" aria-label="Choose a testimonial">
''' + "\n".join(thumb(i, p) for i, p in enumerate(PEOPLE)) + '''
        </div>
      </div>
    </section>'''

h = open("index.html", encoding="utf-8").read()

# 1. remove existing films section entirely
fs = h.find('<section class="films" id="films">')
fe = h.find("</section>", fs) + len("</section>")
assert fs > 0
h = h[:fs] + h[fe:]
# tidy leftover comment line for films if present
h = h.replace("<!-- ───────────── 02 · CASE FILMS ───────────── -->\n", "")

# 2. insert new section right BEFORE the problem section (i.e. directly under hero)
ps = h.find('<section class="problem" id="problem">')
assert ps > 0
# find any preceding comment marker for problem to insert before it cleanly
pc = h.rfind("<!--", 0, ps)
ins = pc if (pc > 0 and "PROBLEM" in h[pc:ps].upper()) else ps
h = h[:ins] + SECTION + "\n\n    " + h[ins:]

# 3. renumber: problem becomes 02
h = h.replace(">01 — The problem<", ">02 — The problem<")

open("index.html", "w", encoding="utf-8").write(h)
print("section rebuilt + moved under hero")

# 4. CSS
css = open("css/main.css", encoding="utf-8").read()
if ".cine__stage" not in css:
    css += """

/* ── cinema testimonial stage ── */
.cine { margin-top: clamp(2.5rem, 5vh, 4rem); }
.cine__stage { display: grid; grid-template-columns: minmax(280px, 400px) 1fr; gap: clamp(2.5rem, 6vw, 6rem); align-items: center; max-width: 1180px; }
.cine__framewrap { position: relative; }
.cine__glow { position: absolute; inset: -18%; background: radial-gradient(closest-side, rgba(255,128,0,0.22), transparent 70%); filter: blur(30px); pointer-events: none; }
.cine__frame {
  position: relative; aspect-ratio: 9 / 16; border-radius: 22px; overflow: hidden;
  background: var(--ink-2); border: 1px solid rgba(255,128,0,0.35);
  box-shadow: 0 50px 140px -40px rgba(255,128,0,0.35), 0 30px 80px rgba(0,0,0,0.65);
  transform: rotate(-1.2deg);
  transition: transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.cine__frame:hover { transform: rotate(0deg) scale(1.01); }
.cine__frame.playing { transform: rotate(0deg); }
.cine__frame img, .cine__frame video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.cine__frame::after { content: ""; position: absolute; inset: 0; border-radius: inherit; box-shadow: inset 0 0 0 1px rgba(242,237,230,0.08), inset 0 -80px 90px -60px rgba(0,0,0,0.7); pointer-events: none; }
.cine__frame.playing::after { display: none; }
.cine__play {
  position: absolute; inset: 0; margin: auto; width: 84px; height: 84px; z-index: 2;
  border-radius: 50%; border: 0; cursor: pointer; background: var(--orange); color: var(--ink);
  display: grid; place-items: center; transition: transform 0.25s ease, background 0.25s ease;
}
.cine__play:hover { transform: scale(1.1); background: var(--orange-up); }
.cine__playicon { font-size: 1.5rem; margin-left: 4px; }
.cine__playring { position: absolute; inset: -10px; border-radius: 50%; border: 1px solid rgba(255,128,0,0.55); animation: cinepulse 2.2s ease-out infinite; }
@keyframes cinepulse { 0% { transform: scale(0.9); opacity: 1; } 100% { transform: scale(1.45); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .cine__playring { animation: none; } }

.cine__metric { font-family: var(--display); font-weight: 800; font-size: clamp(3.4rem, 7.5vw, 6.2rem); line-height: 0.95; letter-spacing: -0.02em; color: var(--orange); }
.cine__mlabel { font-family: var(--display); font-weight: 500; font-size: clamp(0.95rem, 1.4vw, 1.15rem); letter-spacing: 0.02em; color: var(--paper); margin-top: 0.5rem; }
.cine__quote { font-family: var(--serif); font-style: italic; font-size: clamp(1.25rem, 2vw, 1.7rem); line-height: 1.4; color: var(--grey); margin-top: 1.6rem; max-width: 24ch; }
.cine__who { margin-top: 1.6rem; }
.cine__who strong { font-family: var(--display); font-weight: 700; font-size: 1.02rem; display: block; }
.cine__who span { font-size: 0.84rem; color: var(--grey-dim); }
.cine__veri { margin-top: 1.1rem; font-size: 0.78rem; color: var(--grey-dim); letter-spacing: 0.04em; }
.cine__stars { color: var(--orange); letter-spacing: 0.2em; }
.cine--noquote .cine__metric, .cine--noquote .cine__mlabel { display: none; }
.cine--noquote .cine__quote { margin-top: 0; }

.cine__rail { display: flex; gap: 0.9rem; margin-top: clamp(2rem, 4vh, 3rem); overflow-x: auto; padding: 0.5rem 0.25rem 1rem; scroll-snap-type: x proximity; scrollbar-width: none; }
.cine__rail::-webkit-scrollbar { display: none; }
.cine__thumb {
  flex: 0 0 104px; scroll-snap-align: start; border: 0; background: none; padding: 0; cursor: pointer;
  font-family: var(--display); color: var(--grey-dim); font-size: 0.72rem; letter-spacing: 0.04em; text-align: center;
}
.cine__thumb img {
  width: 104px; aspect-ratio: 9 / 16; object-fit: cover; border-radius: 14px; display: block;
  border: 1px solid var(--line); opacity: 0.55; filter: saturate(0.7);
  transition: opacity 0.25s ease, transform 0.25s ease, border-color 0.25s ease, filter 0.25s ease;
}
.cine__thumb span { display: block; margin-top: 0.5rem; }
.cine__thumb:hover img { opacity: 0.9; transform: translateY(-4px); }
.cine__thumb.is-active img { opacity: 1; filter: none; border-color: var(--orange); box-shadow: 0 12px 40px -12px rgba(255,128,0,0.45); }
.cine__thumb.is-active { color: var(--paper); }

@media (max-width: 900px) {
  .cine__stage { grid-template-columns: 1fr; gap: 2rem; }
  .cine__framewrap { max-width: 300px; margin: 0 auto; width: 100%; }
  .cine__quote { max-width: none; }
}
"""
    open("css/main.css", "w", encoding="utf-8").write(css)
    print("css appended")

# 5. JS: remove old wall handler, add cinema controller
js = open("js/main.js", encoding="utf-8").read()
old = js.find("/* ── testimonial wall: click-to-play, one at a time ── */")
if old > 0:
    oldend = js.find("  });\n  });\n", old)
    if oldend > 0:
        js = js[:old] + js[oldend + len("  });\n  });\n"):]
        print("old wall js removed")

if "cine-rail" not in js:
    hook = """
  /* ── cinema testimonials: stage + filmstrip ── */
  (function () {
    var rail = document.getElementById("cine-rail");
    if (!rail) return;
    var frame = document.getElementById("cine-frame");
    var poster = document.getElementById("cine-poster");
    var play = document.getElementById("cine-play");
    var stage = document.querySelector(".cine__stage");
    var metric = document.getElementById("cine-metric");
    var mlabel = document.getElementById("cine-mlabel");
    var quote = document.getElementById("cine-quote");
    var nameEl = document.getElementById("cine-name");
    var coEl = document.getElementById("cine-co");
    var current = rail.querySelector(".cine__thumb.is-active");

    function stopVideo() {
      var v = frame.querySelector("video");
      if (v) { v.pause(); v.remove(); }
      frame.classList.remove("playing");
      poster.style.display = "";
      play.style.display = "";
    }

    function applyMeta(btn) {
      var m = btn.dataset.metric, q = btn.dataset.quote;
      metric.textContent = m;
      mlabel.textContent = btn.dataset.mlabel;
      quote.innerHTML = q ? "\\u201C" + q + "\\u201D" : "Real client. Real story. Press play.";
      nameEl.textContent = btn.dataset.name;
      coEl.textContent = btn.dataset.co;
      stage.classList.toggle("cine--noquote", !m);
    }

    rail.addEventListener("click", function (e) {
      var btn = e.target.closest(".cine__thumb");
      if (!btn || btn === current) return;
      stopVideo();
      current.classList.remove("is-active");
      btn.classList.add("is-active");
      current = btn;
      poster.src = btn.dataset.jpg;
      applyMeta(btn);
    });

    play.addEventListener("click", function () {
      var v = document.createElement("video");
      v.src = current.dataset.mp4;
      v.controls = true; v.autoplay = true; v.playsInline = true;
      frame.appendChild(v);
      frame.classList.add("playing");
      poster.style.display = "none";
      play.style.display = "none";
      v.addEventListener("ended", stopVideo);
    });
  })();
"""
    anchor = "  /* ── qualifier: live routing + submit ──"
    assert anchor in js
    js = js.replace(anchor, hook + "\n" + anchor)
    open("js/main.js", "w", encoding="utf-8").write(js)
    print("cinema js added")

print("CINEMA PATCH DONE")
