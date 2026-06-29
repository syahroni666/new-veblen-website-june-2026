# -*- coding: utf-8 -*-
"""Proof packs: Bish NETWRK brief + Crown video-production captions (homepage),
LCMB + NTT case-page media sections (generator), player + siteshot styles."""

# ── 1. homepage: Bish brief + Crown captions ──
h = open("index.html", encoding="utf-8").read()

bish_old = '''          <figcaption><p class="ct__who"><strong>Bishoy</strong><span>TalentPort · Talent Placement</span></p></figcaption>'''
bish_new = '''          <figcaption>
            <p class="ct__who"><strong>Bishoy</strong><span>TalentPort · Talent Placement</span></p>
            <a class="ct__built" href="https://phones.veblengroup.com.au" target="_blank" rel="noopener">
              <img src="assets/sites/netwrk.webp" alt="NETWRK Phone Systems website built by Veblen" loading="lazy" decoding="async" />
              <span><b>We build for them too</b>NETWRK Phone Systems — site by Veblen</span>
            </a>
          </figcaption>'''
assert bish_old in h
h = h.replace(bish_old, bish_new)

h = h.replace('<figcaption><p class="ct__who"><strong>Ardy</strong><span>Crown Realty · Real Estate</span></p></figcaption>',
              '<figcaption><p class="ct__who"><strong>Ardy</strong><span>Crown Realty · Real Estate</span><em class="ct__tag">Video production by Veblen</em></p></figcaption>')
h = h.replace('<figcaption><p class="ct__who"><strong>Kento</strong><span>Crown Realty · Real Estate</span></p></figcaption>',
              '<figcaption><p class="ct__who"><strong>Kento</strong><span>Crown Realty · Real Estate</span><em class="ct__tag">Video production by Veblen</em></p></figcaption>')
open("index.html", "w", encoding="utf-8").write(h)
print("homepage: bish brief + crown tags")

css = open("css/main.css", encoding="utf-8").read()
if ".ct__built" not in css:
    css += """
/* built-by-veblen mini brief on testimonial cards */
.ct__tag { display: block; font-style: normal; color: var(--orange); font-size: 0.72rem; margin-top: 0.2rem; }
.ct__built { display: flex; gap: 0.7rem; align-items: center; margin-top: 0.8rem; padding: 0.6rem; border: 1px solid var(--line); border-radius: 12px; text-decoration: none; color: var(--grey); transition: border-color 0.25s ease, transform 0.25s ease; }
.ct__built:hover { border-color: var(--orange); transform: translateY(-2px); }
.ct__built img { width: 52px; height: 78px; object-fit: cover; object-position: top; border-radius: 7px; border: 1px solid var(--line); }
.ct__built span { font-size: 0.7rem; line-height: 1.35; letter-spacing: 0.02em; }
.ct__built b { display: block; font-family: var(--display); font-weight: 700; color: var(--paper); font-size: 0.74rem; margin-bottom: 0.15rem; }
"""
    open("css/main.css", "w", encoding="utf-8").write(css)
    print("homepage css ok")

# ── 2. generator: LCMB + NTT media sections ──
p = "tools/build_pages.py"
s = open(p, encoding="utf-8").read()

LCMB_EXTRA = '''
<section class="psec--tint psec"><div class="psec__in">
  <h2>Everything we run for LCMB.</h2>
  <p class="lead">Not a service here and a service there — one engine, every part feeding the next.</p>
  {fcards([
    ('<span class="n">01</span>Meta-first lead generation', "Campaigns per service line with high-intent, qualifying lead forms."),
    ('<span class="n">02</span>Creative on real jobs', "Ad creative shot with LCMB crews on LCMB installs — no stock footage."),
    ('<span class="n">03</span>CRM + AI follow-up', "One pipeline, every enquiry answered in under 60 seconds, day or night."),
    ('<span class="n">04</span>Conversion-built website', "A ground-up rebuild of lcmbgroup.com.au, engineered to turn visits into booked jobs."),
    ('<span class="n">05</span>Reviews &amp; local search', "Review engine and Google Business Profile foundations feeding the map pack."),
    ('<span class="n">06</span>Performance reporting', "Decisions made on live CPL and booked-job data — reported in dollars, not impressions."),
  ])}
  <div class="mediarow">
    <figure class="vcard">
      <div class="vcard__frame">
        <img src="https://media.veblengroup.com.au/site/testimonials/luke-lcmb.jpg" alt="Luke Muir, LCMB Group" loading="lazy" decoding="async" />
        <button class="vcard__play" type="button" data-vplay="https://media.veblengroup.com.au/site/testimonials/luke-lcmb.mp4" aria-label="Play Luke Muir testimonial">▶</button>
      </div>
      <figcaption>Luke Muir on what changed — on camera, unscripted.</figcaption>
    </figure>
    <a class="siteshot" href="https://lcmb-website-preview.vercel.app" target="_blank" rel="noopener">
      <span class="siteshot__bar"><i></i><i></i><i></i><b>lcmbgroup.com.au — the rebuild</b></span>
      <img src="/assets/sites/lcmb-new.webp" alt="New LCMB Group website built by Veblen" loading="lazy" decoding="async" />
      <span class="siteshot__cap"><strong>The new LCMB site</strong>Designed and built by Veblen — fast, proof-led, made to convert.</span>
    </a>
  </div>
</div></section>
'''

NTT_EXTRA = '''
<section class="psec--tint psec"><div class="psec__in">
  <h2>Everything we run for NT Trailers.</h2>
  <p class="lead">Volume out front, infrastructure behind it — and a creative production line keeping the ads sharp at 600 leads a month.</p>
  {fcards([
    ('<span class="n">01</span>Meta-first campaigns at scale', "Product-led creative tested and rotated continuously — the ads keep getting sharper."),
    ('<span class="n">02</span>Social video production', "A steady line of short-form video built around the trailers and the people who buy them."),
    ('<span class="n">03</span>Complete CRM build', "Enquiry → qualification → quote → deposit, every stage visible and automated."),
    ('<span class="n">04</span>Automated nurture', "Instant first response, then structured follow-up that holds buyers through the comparison weeks."),
    ('<span class="n">05</span>Website', "NT Trailers' site, built by Veblen to carry paid traffic and convert considered buyers."),
    ('<span class="n">06</span>Live attribution', "Spend decisions made on cost per lead and deposits, not clicks."),
  ])}
  <div class="mediarow">
    <figure class="vcard">
      <div class="vcard__frame">
        <img src="https://media.veblengroup.com.au/site/testimonials/josh-nt-trailers.jpg" alt="Josh Norris, NT Trailers" loading="lazy" decoding="async" />
        <button class="vcard__play" type="button" data-vplay="https://media.veblengroup.com.au/site/testimonials/josh-nt-trailers.mp4" aria-label="Play Josh Norris testimonial">▶</button>
      </div>
      <figcaption>Josh Norris on the fullest pipeline in company history.</figcaption>
    </figure>
    <a class="siteshot" href="https://nttrailers.com.au" target="_blank" rel="noopener">
      <span class="siteshot__bar"><i></i><i></i><i></i><b>nttrailers.com.au</b></span>
      <img src="/assets/sites/ntt.webp" alt="NT Trailers website built by Veblen" loading="lazy" decoding="async" />
      <span class="siteshot__cap"><strong>The NT Trailers site</strong>Built by Veblen to carry 600 leads a month of paid traffic.</span>
    </a>
  </div>
</div></section>
'''

a1 = '''</section>
""",
))

# ───────────────────────── 13 · case study: NT Trailers'''
assert a1 in s
s = s.replace(a1, '''</section>
''' + LCMB_EXTRA + '''""",
))

# ───────────────────────── 13 · case study: NT Trailers''')

a2 = '''</section>
""",
))

# ───────────────────────── 14 · case study: ADV+ Painting'''
assert a2 in s
s = s.replace(a2, '''</section>
''' + NTT_EXTRA + '''""",
))

# ───────────────────────── 14 · case study: ADV+ Painting''')
open(p, "w", encoding="utf-8").write(s)
print("generator: lcmb + ntt media sections in")

# ── 3. pages.css: player + siteshot ──
pc = open("css/pages.css", encoding="utf-8").read()
if ".vcard__frame" not in pc:
    pc += """
/* media row: testimonial player + site screenshot */
.mediarow { display: grid; grid-template-columns: minmax(220px, 300px) 1fr; gap: 1.6rem; margin-top: 2.4rem; align-items: start; }
@media (max-width: 760px) { .mediarow { grid-template-columns: 1fr; } }
.vcard { margin: 0; }
.vcard__frame { position: relative; aspect-ratio: 9 / 16; border-radius: 16px; overflow: hidden; background: var(--ink-2); border: 1px solid rgba(255,128,0,0.3); box-shadow: 0 30px 80px -25px rgba(0,0,0,0.7); }
.vcard__frame img, .vcard__frame video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.vcard__play { position: absolute; inset: 0; margin: auto; width: 62px; height: 62px; border-radius: 50%; border: 0; cursor: pointer; background: var(--orange); color: var(--ink); font-size: 1.1rem; display: grid; place-items: center; transition: transform 0.25s ease; }
.vcard__play:hover { transform: scale(1.1); }
.vcard figcaption { font-size: 0.82rem; color: var(--grey-dim); margin-top: 0.7rem; }
.siteshot { display: block; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; text-decoration: none; color: var(--grey); background: var(--ink); transition: border-color 0.25s ease, transform 0.25s ease; }
.siteshot:hover { border-color: var(--orange); transform: translateY(-3px); }
.siteshot__bar { display: flex; align-items: center; gap: 0.35rem; padding: 0.55rem 0.8rem; border-bottom: 1px solid var(--line); background: var(--ink-2); }
.siteshot__bar i { width: 9px; height: 9px; border-radius: 50%; background: var(--grey-dim); opacity: 0.5; }
.siteshot__bar b { margin-left: 0.5rem; font-family: var(--display); font-weight: 500; font-size: 0.74rem; color: var(--grey-dim); letter-spacing: 0.03em; }
.siteshot > img { width: 100%; max-height: 330px; object-fit: cover; object-position: top; display: block; }
.siteshot__cap { display: block; padding: 0.9rem 1rem; font-size: 0.8rem; line-height: 1.4; }
.siteshot__cap strong { display: block; font-family: var(--display); font-weight: 700; color: var(--paper); font-size: 0.88rem; margin-bottom: 0.15rem; }
"""
    open("css/pages.css", "w", encoding="utf-8").write(pc)
    print("pages.css ok")

# ── 4. page.js: in-place player ──
pj = open("js/page.js", encoding="utf-8").read()
if "data-vplay" not in pj:
    hook = """
  // in-place testimonial players on case pages
  document.querySelectorAll(".vcard__play[data-vplay]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var frame = btn.closest(".vcard__frame");
      var v = document.createElement("video");
      v.src = btn.dataset.vplay;
      v.controls = true; v.autoplay = true; v.playsInline = true;
      v.style.cssText = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover;";
      frame.appendChild(v);
      btn.style.display = "none";
      v.addEventListener("ended", function () { v.remove(); btn.style.display = ""; });
    });
  });
"""
    anchor = '  // lead form (one per page; entryPath carries the page slug)'
    assert anchor in pj
    pj = pj.replace(anchor, hook + "\n" + anchor)
    open("js/page.js", "w", encoding="utf-8").write(pj)
    print("page.js ok")

print("PROOFPACK DONE")
