# -*- coding: utf-8 -*-
"""Testimonials v5 — research-backed phone-frame grid.
Pattern (Directive/NoGood/King Kong + CRO consensus): phones ~260px in CSS device
frames, muted 5s autoplay preview loops, click = full video with sound, metric in
bold type below each phone. Proof-first hierarchy. Replaces dossiers + quartet."""

BASE = "https://media.veblengroup.com.au/site/testimonials"

ROW1 = [
    ("josh-nt-trailers", "Josh Norris", "NT Trailers", "600", "leads a month at under $32 CPL",
     "NT Trailers has never had a pipeline this full."),
    ("luke-lcmb", "Luke Muir", "LCMB Group", "100+", "qualified leads, every month",
     "Jobs booked before a competitor even sees them."),
    ("david-adv-painting", "David", "ADV+ Painting", "$0→$50k", "monthly revenue, from zero online",
     "The system they built is genuinely incredible."),
]
ROW2 = [
    ("streamline-plumbing", "Streamline Plumbing", "Plumbing · Trades", ""),
    ("ardy-crown-realty", "Ardy", "Crown Realty", "Video production client"),
    ("kento-crown-realty", "Kento", "Crown Realty", "Video production client"),
    ("bish-talentport", "Bishoy", "TalentPort", ""),
]

def phone(slug, label):
    return f'''            <div class="ph__shell">
              <button class="ph" type="button" data-full="{BASE}/{slug}.mp4" data-preview="{BASE}/{slug}-preview.mp4" data-poster="{BASE}/{slug}.jpg" aria-label="Watch {label} testimonial">
                <span class="ph__screen">
                  <img src="{BASE}/{slug}.jpg" alt="{label} video testimonial" loading="lazy" decoding="async" />
                  <span class="ph__sound" aria-hidden="true">🔊&nbsp;Tap for sound</span>
                </span>
                <span class="ph__island" aria-hidden="true"></span>
              </button>
            </div>'''

def big_card(slug, name, co, metric, mlabel, quote):
    return f'''          <figure class="pcard pcard--big" data-reveal>
{phone(slug, name)}
            <figcaption>
              <p class="pcard__metric">{metric}</p>
              <p class="pcard__mlabel">{mlabel}</p>
              <p class="pcard__quote">&ldquo;{quote}&rdquo;</p>
              <p class="pcard__who"><strong>{name}</strong><span>{co}</span></p>
            </figcaption>
          </figure>'''

def sm_card(slug, name, co, tag):
    tagline = f'<em class="pcard__tag">{tag}</em>' if tag else ""
    extra = ""
    if slug == "bish-talentport":
        extra = '<a class="pcard__link" href="https://phones.veblengroup.com.au" target="_blank" rel="noopener">+ we built NETWRK\'s site →</a>'
    return f'''          <figure class="pcard pcard--sm" data-reveal>
{phone(slug, name)}
            <figcaption>
              <p class="pcard__who"><strong>{name}</strong><span>{co}</span>{tagline}</p>
              {extra}
            </figcaption>
          </figure>'''

SECTION_INNER = '''
      <div class="phgrid">
        <div class="phgrid__row phgrid__row--hero">
''' + "\n".join(big_card(*c) for c in ROW1) + '''
        </div>
        <div class="phgrid__row phgrid__row--sm">
''' + "\n".join(sm_card(*c) for c in ROW2) + '''
        </div>
        <p class="phgrid__veri" data-reveal><span>★★★★★</span> 5.0 across 16 Google reviews · every face here is a real client · <a href="/case-studies/">read the full case studies →</a></p>
      </div>
    </section>'''

h = open("index.html", encoding="utf-8").read()
fs = h.find('<section class="films" id="films">')
fe = h.find("</section>", fs) + len("</section>")
assert fs > 0
head_end = h.find('<div class="ctwall">', fs)
assert fs < head_end < fe
new_section = h[fs:head_end] + SECTION_INNER[SECTION_INNER.find('<div class="phgrid">'):]
h = h[:fs] + new_section + h[fe:]
open("index.html", "w", encoding="utf-8").write(h)
print("phone grid section in")

css = open("css/main.css", encoding="utf-8").read()
if ".ph__screen" not in css:
    css += """

/* ── phone-frame testimonial grid (research-backed v5) ── */
.phgrid { margin-top: clamp(2.5rem, 5vh, 4rem); }
.phgrid__row--hero { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(1.6rem, 3vw, 2.8rem); max-width: 1180px; }
.phgrid__row--sm { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(1.2rem, 2.4vw, 2rem); margin-top: clamp(2.6rem, 5vh, 4rem); max-width: 1180px; }
.pcard { margin: 0; text-align: left; }
.ph__shell { position: relative; max-width: 250px; }
.pcard--sm .ph__shell { max-width: 190px; }
.ph {
  position: relative; display: block; width: 100%; padding: 9px; cursor: pointer;
  background: #050403; border: 1px solid rgba(242,237,230,0.13); border-radius: 40px;
  box-shadow: 0 30px 70px -25px rgba(0,0,0,0.85), 0 4px 18px rgba(0,0,0,0.5);
  transition: transform 0.35s cubic-bezier(0.2, 0.7, 0.2, 1), border-color 0.3s ease, box-shadow 0.35s ease;
}
.pcard--sm .ph { border-radius: 32px; padding: 7px; }
.ph:hover { transform: translateY(-6px); border-color: rgba(255,128,0,0.5); box-shadow: 0 38px 80px -25px rgba(255,128,0,0.18), 0 30px 70px -25px rgba(0,0,0,0.85); }
.ph__screen { position: relative; display: block; aspect-ratio: 9 / 16; border-radius: 31px; overflow: hidden; background: var(--ink-2); }
.pcard--sm .ph__screen { border-radius: 25px; }
.ph__screen img, .ph__screen video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.ph__island { position: absolute; top: 17px; left: 50%; transform: translateX(-50%); width: 64px; height: 17px; border-radius: 999px; background: #050403; border: 1px solid rgba(242,237,230,0.08); z-index: 3; }
.pcard--sm .ph__island { width: 50px; height: 14px; top: 14px; }
.ph__sound {
  position: absolute; left: 50%; bottom: 12px; transform: translateX(-50%);
  font-family: var(--display); font-weight: 600; font-size: 0.62rem; letter-spacing: 0.06em;
  color: var(--paper); background: rgba(5,4,3,0.72); backdrop-filter: blur(6px);
  border: 1px solid rgba(242,237,230,0.14); border-radius: 999px; padding: 0.32rem 0.7rem;
  white-space: nowrap; opacity: 0; transition: opacity 0.3s ease; z-index: 3;
}
.ph.previewing .ph__sound { opacity: 1; }
.ph.fullplay .ph__sound { display: none; }
.pcard figcaption { padding: 1.2rem 0.2rem 0; max-width: 250px; }
.pcard--sm figcaption { max-width: 190px; }
.pcard__metric { font-family: var(--display); font-weight: 800; font-size: clamp(2.2rem, 3.6vw, 3.2rem); line-height: 1; letter-spacing: -0.02em; color: var(--orange); }
.pcard__mlabel { font-family: var(--display); font-weight: 500; font-size: 0.88rem; line-height: 1.45; color: var(--paper); margin-top: 0.45rem; }
.pcard__quote { font-family: var(--serif); font-style: italic; font-size: 0.98rem; line-height: 1.5; color: var(--grey); margin-top: 0.8rem; }
.pcard__who { margin-top: 0.8rem; font-size: 0.76rem; }
.pcard__who strong { font-family: var(--display); font-weight: 700; color: var(--paper); display: block; font-size: 0.86rem; }
.pcard__who span { color: var(--grey-dim); }
.pcard__tag { display: block; font-style: normal; color: var(--orange); font-size: 0.7rem; margin-top: 0.2rem; }
.pcard__link { display: inline-block; margin-top: 0.5rem; font-family: var(--display); font-weight: 600; font-size: 0.72rem; color: var(--orange); text-decoration: none; }
.pcard__link:hover { text-decoration: underline; }
.phgrid__veri { margin-top: clamp(2.2rem, 4vh, 3.2rem); font-size: 0.8rem; color: var(--grey-dim); letter-spacing: 0.04em; }
.phgrid__veri span { color: var(--orange); letter-spacing: 0.2em; margin-right: 0.4rem; }
.phgrid__veri a { color: var(--orange); text-decoration: none; }
.phgrid__veri a:hover { text-decoration: underline; }
@media (max-width: 940px) {
  .phgrid__row--hero { grid-template-columns: 1fr; justify-items: center; }
  .phgrid__row--hero .pcard { display: grid; grid-template-columns: minmax(150px, 200px) 1fr; gap: 1.4rem; align-items: center; width: 100%; max-width: 480px; }
  .phgrid__row--hero figcaption { padding-top: 0; }
  .phgrid__row--sm { grid-template-columns: 1fr 1fr; justify-items: center; }
  .phgrid__row--sm .pcard { text-align: center; }
  .phgrid__row--sm .ph__shell, .phgrid__row--sm figcaption { margin: 0 auto; }
}
"""
    open("css/main.css", "w", encoding="utf-8").write(css)
    print("phone css in")

js = open("js/main.js", encoding="utf-8").read()
# remove the dossier/ct player handler
a = js.find('  /* ── testimonial wall: in-place players, one at a time ── */')
if a > 0:
    b = js.find("  });\n  });\n", a)
    js = js[:a] + js[b + len("  });\n  });\n"):]
    print("old ct js removed")
if "data-preview" not in js:
    hook = """
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

    phones.forEach(function (p) {
      p.addEventListener("click", function () {
        if (p.classList.contains("fullplay")) return;
        stopFull();
        var prev = p.querySelector("video");
        if (prev) prev.remove();
        p.classList.remove("previewing");
        var v = document.createElement("video");
        v.src = p.dataset.full;
        v.poster = p.dataset.poster;
        v.controls = true; v.autoplay = true; v.playsInline = true;
        p.querySelector(".ph__screen").appendChild(v);
        p.classList.add("fullplay");
        v.addEventListener("ended", function () {
          v.remove(); p.classList.remove("fullplay"); startPreview(p);
        });
      });
    });
  })();
"""
    anchor = "  /* ── qualifier: live routing + submit ──"
    assert anchor in js
    js = js.replace(anchor, hook + "\n" + anchor)
    open("js/main.js", "w", encoding="utf-8").write(js)
    print("phone js in")
print("PHONE GRID DONE")
