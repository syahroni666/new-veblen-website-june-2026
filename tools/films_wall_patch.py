# -*- coding: utf-8 -*-
"""Swap Drive-linked film grid for clean R2 click-to-play testimonial wall."""
import re

BASE = "https://media.veblengroup.com.au/site/testimonials"

TILES = [
    ("luke-lcmb", "Luke Muir", "LCMB Group · Electrical &amp; Air Conditioning", "100+ qualified leads, every month"),
    ("josh-nt-trailers", "Josh Norris", "NT Trailers · Trailer Manufacturing", "600 leads a month at under $32 CPL"),
    ("david-adv-painting", "David", "ADV+ Painting · Painting", "$0 to $50k months"),
    ("ardy-crown-realty", "Ardy", "Crown Realty · Real Estate", ""),
    ("kento-crown-realty", "Kento", "Crown Realty · Real Estate", ""),
    ("bish-talentport", "Bishoy", "TalentPort · Talent Placement", ""),
]

def tile(slug, name, role, result):
    em = f"<em>{result}</em>" if result else ""
    return f'''        <figure class="film film--t" data-reveal>
          <button class="film__poster" type="button" data-mp4="{BASE}/{slug}.mp4" aria-label="Play {name} testimonial">
            <img src="{BASE}/{slug}.jpg" alt="{name} — {role.replace('&amp;', 'and')}" loading="lazy" decoding="async" />
            <span class="film__play">▶</span>
          </button>
          <figcaption><strong>{name}</strong><span>{role}</span>{em}</figcaption>
        </figure>'''

h = open("index.html", encoding="utf-8").read()
start = h.find('<div class="films__grid">')
assert start > 0
end = h.find("</section>", start)
assert end > start
grid = '<div class="films__grid">\n' + "\n".join(tile(*t) for t in TILES) + "\n      </div>\n    "
h = h[:start] + grid + h[end:]
open("index.html", "w", encoding="utf-8").write(h)
print("films grid replaced: 6 R2 tiles")

css = open("css/main.css", encoding="utf-8").read()
if ".film--t" not in css:
    css += """

/* ── testimonial wall (R2 click-to-play) ── */
.film--t { grid-column: span 2 !important; }
.film__poster { display: block; width: 100%; border: 1px solid var(--line); background: var(--ink-2); padding: 0; cursor: pointer; font: inherit; color: inherit; }
.film__poster img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.film__poster.playing .film__play, .film__poster.playing img { display: none; }
.film figcaption em { display: block; color: var(--orange); font-style: normal; font-size: 0.82rem; margin-top: 0.15rem; }
@media (max-width: 860px) { .film--t { grid-column: span 3 !important; } }
"""
    open("css/main.css", "w", encoding="utf-8").write(css)
    print("css appended")

js = open("js/main.js", encoding="utf-8").read()
if "data-mp4" not in js:
    hook = """
  /* ── testimonial wall: click-to-play, one at a time ── */
  document.querySelectorAll(".film__poster[data-mp4]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".film__poster video").forEach(function (old) {
        old.pause(); old.parentElement.classList.remove("playing"); old.remove();
      });
      var v = document.createElement("video");
      v.src = btn.dataset.mp4;
      v.controls = true; v.autoplay = true; v.playsInline = true;
      v.style.cssText = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover;";
      btn.classList.add("playing");
      btn.appendChild(v);
      v.addEventListener("ended", function () { btn.classList.remove("playing"); v.remove(); });
    });
  });
"""
    # insert before the qualifier block
    anchor = "  /* ── qualifier: live routing + submit ──"
    assert anchor in js
    js = js.replace(anchor, hook + "\n" + anchor)
    open("js/main.js", "w", encoding="utf-8").write(js)
    print("js appended")
print("PATCH DONE")
