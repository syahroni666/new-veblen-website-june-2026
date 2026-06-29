# -*- coding: utf-8 -*-
"""Testimonials v4 — Fortune-500 case dossiers: video | story + what-we-built | site shot.
Replaces the oversized triptych. Quartet row below is retained."""

BASE = "https://media.veblengroup.com.au/site/testimonials"

DOSSIERS = [
    dict(slug="luke-lcmb", name="Luke Muir", client="LCMB GROUP",
         meta="Electrical · Air Conditioning · Solar — Gold Coast + Brisbane",
         about="A multi-crew electrical and air conditioning operation running service lines across two cities.",
         metric="100+", mlabel="qualified leads, every month",
         quote="Jobs booked automatically before a competitor even sees the notification.",
         chips=["Meta-first lead generation", "High-intent forms", "CRM + AI follow-up &lt;60s", "Creative on real jobs", "Website rebuild", "Reviews &amp; local search"],
         shot="/assets/sites/lcmb-new.webp", shoturl="https://lcmb-website-preview.vercel.app",
         shotbar="lcmbgroup.com.au — the rebuild", shotcap="New site, designed + built by Veblen",
         case="/case-studies/lcmb/"),
    dict(slug="josh-nt-trailers", name="Josh Norris", client="NT TRAILERS",
         meta="Trailer Manufacturing — Darwin, shipping Australia-wide",
         about="A manufacturer selling a considered, high-ticket product to buyers who compare for weeks.",
         metric="600", mlabel="leads a month at under $32 CPL",
         quote="NT Trailers has never had a pipeline this full. These guys deliver.",
         chips=["Meta campaigns at scale", "Social video production", "Complete CRM build", "Automated nurture", "Website", "Live attribution"],
         shot="/assets/sites/ntt.webp", shoturl="https://nttrailers.com.au",
         shotbar="nttrailers.com.au", shotcap="Built by Veblen to carry 600 leads a month",
         case="/case-studies/nt-trailers/"),
    dict(slug="david-adv-painting", name="David", client="ADV+ PAINTING",
         meta="Painting — Trades",
         about="Quality crews, zero online presence. The engine was built from a standing start.",
         metric="$0→$50k", mlabel="monthly revenue",
         quote="The system they built is genuinely incredible.",
         chips=["Google Ads", "Conversion website", "Missed-call text-back", "Automated follow-up", "Review engine"],
         shot="/assets/sites/adv.webp", shoturl="https://advpainting.com.au",
         shotbar="ADV+ Painting", shotcap="Site + engine, built by Veblen",
         case="/case-studies/adv-painting/"),
]

def dossier(d):
    chips = "".join(f"<span>{c}</span>" for c in d["chips"])
    return f'''        <article class="dossier" data-reveal>
          <div class="dossier__video">
            <div class="ct__frame">
              <img src="{BASE}/{d['slug']}.jpg" alt="{d['name']} — {d['client']} testimonial" loading="lazy" decoding="async" />
              <button class="ct__play" type="button" data-mp4="{BASE}/{d['slug']}.mp4" aria-label="Play {d['name']} testimonial">
                <span class="ct__ring" aria-hidden="true"></span><span class="ct__icon">▶</span>
              </button>
            </div>
          </div>
          <div class="dossier__body">
            <p class="dossier__client">{d['client']}<span>{d['meta']}</span></p>
            <p class="dossier__metric">{d['metric']} <em>{d['mlabel']}</em></p>
            <p class="dossier__quote">&ldquo;{d['quote']}&rdquo;</p>
            <p class="dossier__who">— {d['name']}, on camera</p>
            <p class="dossier__about">{d['about']}</p>
            <div class="dossier__did"><b>What we built</b><div class="dossier__chips">{chips}</div></div>
            <a class="dossier__more" href="{d['case']}">Read the full case study →</a>
          </div>
          <a class="dossier__site" href="{d['shoturl']}" target="_blank" rel="noopener">
            <span class="siteshot__bar"><i></i><i></i><i></i><b>{d['shotbar']}</b></span>
            <img src="{d['shot']}" alt="{d['client']} website built by Veblen" loading="lazy" decoding="async" />
            <span class="dossier__sitecap">{d['shotcap']}</span>
          </a>
        </article>'''

NEW = '<div class="ctwall__dossiers">\n' + "\n".join(dossier(d) for d in DOSSIERS) + "\n        </div>"

h = open("index.html", encoding="utf-8").read()
a = h.find('<div class="ctwall__trio">')
b = h.find('<div class="ctwall__quartet">')
assert 0 < a < b
h = h[:a] + NEW + "\n        " + h[b:]
open("index.html", "w", encoding="utf-8").write(h)
print("dossiers in")

css = open("css/main.css", encoding="utf-8").read()
if ".dossier__client" not in css:
    css += """

/* ── case dossiers (fortune-500 panels) ── */
.ctwall__dossiers { display: grid; gap: clamp(1.4rem, 3vh, 2.2rem); }
.dossier {
  display: grid; grid-template-columns: clamp(200px, 21vw, 270px) 1.15fr 1fr;
  gap: clamp(1.4rem, 2.8vw, 2.6rem); align-items: stretch;
  border: 1px solid var(--line); border-radius: 22px; background: var(--ink-2);
  padding: clamp(1.3rem, 2.6vw, 2.2rem);
  transition: border-color 0.3s ease;
}
.dossier:hover { border-color: rgba(255, 128, 0, 0.4); }
.dossier__video .ct__frame { border-color: rgba(255, 128, 0, 0.3); }
.dossier__body { display: flex; flex-direction: column; min-width: 0; }
.dossier__client { font-family: var(--display); font-weight: 800; font-size: 0.9rem; letter-spacing: 0.14em; color: var(--paper); }
.dossier__client span { display: block; font-weight: 400; letter-spacing: 0.04em; font-size: 0.74rem; color: var(--grey-dim); margin-top: 0.3rem; text-transform: none; }
.dossier__metric { font-family: var(--display); font-weight: 800; font-size: clamp(2.4rem, 4.4vw, 3.8rem); line-height: 1; letter-spacing: -0.02em; color: var(--orange); margin-top: 1.1rem; }
.dossier__metric em { font-style: normal; font-weight: 500; font-size: 0.95rem; letter-spacing: 0; color: var(--paper); display: block; margin-top: 0.4rem; }
.dossier__quote { font-family: var(--serif); font-style: italic; font-size: clamp(1.05rem, 1.6vw, 1.3rem); line-height: 1.45; color: var(--grey); margin-top: 1.1rem; max-width: 36ch; }
.dossier__who { font-size: 0.78rem; color: var(--grey-dim); margin-top: 0.45rem; }
.dossier__about { font-size: 0.88rem; color: var(--grey); margin-top: 0.9rem; max-width: 44ch; }
.dossier__did { margin-top: 1.2rem; }
.dossier__did b { font-family: var(--display); font-weight: 700; font-size: 0.7rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--grey-dim); }
.dossier__chips { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 0.6rem; }
.dossier__chips span { font-family: var(--display); font-weight: 500; font-size: 0.72rem; letter-spacing: 0.03em; color: var(--paper); border: 1px solid rgba(255, 128, 0, 0.35); border-radius: 999px; padding: 0.3rem 0.75rem; }
.dossier__more { margin-top: auto; padding-top: 1.2rem; font-family: var(--display); font-weight: 600; font-size: 0.84rem; color: var(--orange); text-decoration: none; }
.dossier__more:hover { text-decoration: underline; }
.dossier__site { display: flex; flex-direction: column; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; text-decoration: none; background: var(--ink); transition: border-color 0.25s ease, transform 0.25s ease; }
.dossier__site:hover { border-color: var(--orange); transform: translateY(-3px); }
.dossier__site .siteshot__bar { display: flex; align-items: center; gap: 0.35rem; padding: 0.55rem 0.8rem; border-bottom: 1px solid var(--line); background: var(--ink-2); }
.dossier__site .siteshot__bar i { width: 9px; height: 9px; border-radius: 50%; background: var(--grey-dim); opacity: 0.5; }
.dossier__site .siteshot__bar b { margin-left: 0.5rem; font-family: var(--display); font-weight: 500; font-size: 0.72rem; color: var(--grey-dim); letter-spacing: 0.03em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.dossier__site > img { width: 100%; flex: 1; object-fit: cover; object-position: top; display: block; min-height: 0; }
.dossier__sitecap { padding: 0.8rem 1rem; font-size: 0.76rem; color: var(--grey-dim); border-top: 1px solid var(--line); }
@media (max-width: 1080px) {
  .dossier { grid-template-columns: clamp(180px, 26vw, 240px) 1fr; }
  .dossier__site { grid-column: 1 / -1; max-height: 360px; }
  .dossier__site > img { max-height: 250px; }
}
@media (max-width: 640px) {
  .dossier { grid-template-columns: 1fr; }
  .dossier__video { max-width: 240px; }
}
"""
    open("css/main.css", "w", encoding="utf-8").write(css)
    print("dossier css in")
print("DOSSIER PATCH DONE")
