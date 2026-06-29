# -*- coding: utf-8 -*-
"""Testimonials v3: full-width triptych (3 metric clients) + quartet row (other 4).
Replaces the single-stage cinema layout."""

BASE = "https://media.veblengroup.com.au/site/testimonials"

TRIO = [
    ("luke-lcmb", "Luke Muir", "LCMB Group · Electrical &amp; Air", "100+", "qualified leads, every month",
     "Jobs booked before a competitor even sees the notification."),
    ("josh-nt-trailers", "Josh Norris", "NT Trailers · Manufacturing", "600", "leads a month at under $32 CPL",
     "NT Trailers has never had a pipeline this full."),
    ("david-adv-painting", "David", "ADV+ Painting · Trades", "$0→$50k", "monthly revenue, from zero online",
     "The system they built is genuinely incredible."),
]
QUARTET = [
    ("streamline-plumbing", "Streamline Plumbing", "Plumbing · Trades"),
    ("ardy-crown-realty", "Ardy", "Crown Realty · Real Estate"),
    ("kento-crown-realty", "Kento", "Crown Realty · Real Estate"),
    ("bish-talentport", "Bishoy", "TalentPort · Talent Placement"),
]

def big(slug, name, co, metric, mlabel, quote, pos):
    return f'''        <figure class="ct ct--big ct--{pos}" data-reveal>
          <div class="ct__glow" aria-hidden="true"></div>
          <div class="ct__frame">
            <img src="{BASE}/{slug}.jpg" alt="{name} testimonial" loading="lazy" decoding="async" />
            <button class="ct__play" type="button" data-mp4="{BASE}/{slug}.mp4" aria-label="Play {name} testimonial">
              <span class="ct__ring" aria-hidden="true"></span><span class="ct__icon">▶</span>
            </button>
          </div>
          <figcaption>
            <p class="ct__metric">{metric}</p>
            <p class="ct__mlabel">{mlabel}</p>
            <p class="ct__quote">&ldquo;{quote}&rdquo;</p>
            <p class="ct__who"><strong>{name}</strong><span>{co}</span></p>
          </figcaption>
        </figure>'''

def small(slug, name, co):
    return f'''        <figure class="ct ct--sm" data-reveal>
          <div class="ct__frame">
            <img src="{BASE}/{slug}.jpg" alt="{name} testimonial" loading="lazy" decoding="async" />
            <button class="ct__play" type="button" data-mp4="{BASE}/{slug}.mp4" aria-label="Play {name} testimonial">
              <span class="ct__icon">▶</span>
            </button>
          </div>
          <figcaption><p class="ct__who"><strong>{name}</strong><span>{co}</span></p></figcaption>
        </figure>'''

SECTION = '''<section class="films" id="films">
      <p class="secnum" data-reveal>01 — Proof, on camera</p>
      <h2 data-reveal>Hear it from <em class="serif">them.</em></h2>
      <p class="sub" data-reveal>Real owners, on camera, talking about what actually changed. No scripts, no actors.</p>

      <div class="ctwall">
        <div class="ctwall__trio">
''' + "\n".join(big(*t, pos) for t, pos in zip(TRIO, ["l", "c", "r"])) + '''
        </div>
        <div class="ctwall__quartet">
''' + "\n".join(small(*q) for q in QUARTET) + '''
        </div>
        <p class="ctwall__veri" data-reveal><span>★★★★★</span> 5.0 across 16 Google reviews · every face on this page is a real client</p>
      </div>
    </section>'''

h = open("index.html", encoding="utf-8").read()
fs = h.find('<section class="films" id="films">')
fe = h.find("</section>", fs) + len("</section>")
assert fs > 0
h = h[:fs] + SECTION + h[fe:]
open("index.html", "w", encoding="utf-8").write(h)
print("triptych section in")

css = open("css/main.css", encoding="utf-8").read()
if ".ctwall__trio" not in css:
    css += """

/* ── testimonial triptych wall ── */
.ctwall { margin-top: clamp(2.5rem, 5vh, 4.5rem); }
.ctwall__trio { display: grid; grid-template-columns: 1fr 1.12fr 1fr; gap: clamp(1.2rem, 2.6vw, 2.4rem); align-items: end; }
.ct { margin: 0; position: relative; }
.ct__glow { position: absolute; inset: -12% -12% 18%; background: radial-gradient(closest-side, rgba(255,128,0,0.16), transparent 70%); filter: blur(28px); pointer-events: none; }
.ct__frame {
  position: relative; aspect-ratio: 9 / 16; border-radius: 20px; overflow: hidden;
  background: var(--ink-2); border: 1px solid rgba(242,237,230,0.1);
  box-shadow: 0 36px 90px -30px rgba(0,0,0,0.8);
  transition: transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1), border-color 0.3s ease, box-shadow 0.4s ease;
}
.ct__frame img, .ct__frame video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.ct__frame::after { content: ""; position: absolute; inset: 0; border-radius: inherit; box-shadow: inset 0 0 0 1px rgba(242,237,230,0.07), inset 0 -70px 80px -55px rgba(0,0,0,0.65); pointer-events: none; }
.ct__frame.playing::after { display: none; }
.ct--big .ct__frame { border-color: rgba(255,128,0,0.3); }
.ct--l .ct__frame { transform: rotate(-1.4deg); }
.ct--r .ct__frame { transform: rotate(1.4deg); }
.ct--c { z-index: 2; }
.ct--c .ct__frame { box-shadow: 0 50px 130px -35px rgba(255,128,0,0.3), 0 36px 90px -30px rgba(0,0,0,0.8); }
.ct--c .ct__glow { inset: -16% -16% 14%; background: radial-gradient(closest-side, rgba(255,128,0,0.24), transparent 70%); }
.ct:hover .ct__frame { transform: rotate(0deg) translateY(-6px); border-color: var(--orange); }
.ct__play {
  position: absolute; inset: 0; margin: auto; width: 70px; height: 70px; z-index: 2;
  border-radius: 50%; border: 0; cursor: pointer; background: var(--orange); color: var(--ink);
  display: grid; place-items: center; transition: transform 0.25s ease, background 0.25s ease;
}
.ct--sm .ct__play { width: 54px; height: 54px; }
.ct__play:hover { transform: scale(1.12); background: var(--orange-up); }
.ct__icon { font-size: 1.25rem; margin-left: 3px; }
.ct__ring { position: absolute; inset: -9px; border-radius: 50%; border: 1px solid rgba(255,128,0,0.55); animation: cinepulse 2.2s ease-out infinite; }
.ct figcaption { padding: 1.1rem 0.4rem 0; }
.ct__metric { font-family: var(--display); font-weight: 800; font-size: clamp(1.9rem, 3.4vw, 3rem); line-height: 1; letter-spacing: -0.02em; color: var(--orange); }
.ct__mlabel { font-family: var(--display); font-weight: 500; font-size: 0.86rem; color: var(--paper); margin-top: 0.35rem; }
.ct__quote { font-family: var(--serif); font-style: italic; font-size: 0.98rem; line-height: 1.45; color: var(--grey); margin-top: 0.7rem; }
.ct__who { margin-top: 0.7rem; font-size: 0.78rem; }
.ct__who strong { font-family: var(--display); font-weight: 700; color: var(--paper); display: block; font-size: 0.88rem; }
.ct__who span { color: var(--grey-dim); }
.ctwall__quartet { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(1rem, 2.2vw, 1.8rem); margin-top: clamp(2rem, 4.5vh, 3.5rem); }
.ctwall__veri { margin-top: clamp(1.8rem, 3.5vh, 2.6rem); text-align: center; font-size: 0.8rem; color: var(--grey-dim); letter-spacing: 0.05em; }
.ctwall__veri span { color: var(--orange); letter-spacing: 0.2em; margin-right: 0.4rem; }
@media (max-width: 980px) {
  .ctwall__trio { grid-template-columns: 1fr; max-width: 320px; margin: 0 auto; gap: 2.2rem; }
  .ct--l .ct__frame, .ct--r .ct__frame { transform: none; }
  .ctwall__quartet { grid-template-columns: 1fr 1fr; max-width: 480px; margin: 2.2rem auto 0; }
}
"""
    open("css/main.css", "w", encoding="utf-8").write(css)
    print("css in")

js = open("js/main.js", encoding="utf-8").read()
# remove the single-stage cinema controller
a = js.find('  /* ── cinema testimonials: stage + filmstrip ── */')
if a > 0:
    b = js.find("  })();", a)
    js = js[:a] + js[b + len("  })();\n"):]
    print("old cinema js removed")
if "ct__play" not in js:
    hook = """
  /* ── testimonial wall: in-place players, one at a time ── */
  document.querySelectorAll(".ct__play[data-mp4]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".ct__frame video").forEach(function (old) {
        var fr = old.parentElement;
        old.pause(); old.remove();
        fr.classList.remove("playing");
        fr.querySelector("img").style.display = "";
        var p = fr.querySelector(".ct__play"); if (p) p.style.display = "";
      });
      var frame = btn.closest(".ct__frame");
      var v = document.createElement("video");
      v.src = btn.dataset.mp4;
      v.controls = true; v.autoplay = true; v.playsInline = true;
      frame.appendChild(v);
      frame.classList.add("playing");
      frame.querySelector("img").style.display = "none";
      btn.style.display = "none";
      v.addEventListener("ended", function () {
        v.remove(); frame.classList.remove("playing");
        frame.querySelector("img").style.display = "";
        btn.style.display = "";
      });
    });
  });
"""
    anchor = "  /* ── qualifier: live routing + submit ──"
    assert anchor in js
    js = js.replace(anchor, hook + "\n" + anchor)
    open("js/main.js", "w", encoding="utf-8").write(js)
    print("wall js in")
print("TRIO PATCH DONE")
