# -*- coding: utf-8 -*-
"""Veblen v2 inner-page generator.
Run:  python tools/build_pages.py            (preview build, noindex)
      python tools/build_pages.py --launch   (production build, indexable)
Outputs static pages into the repo root. Claims policy: every number on these
pages must already exist on the live homepage or in an approved vault claim.
"""
import os, sys, json, datetime

NOINDEX = "--launch" not in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://veblengroup.com.au"
BOOK_URL = "https://veblen-platform-production.up.railway.app/book/strategy-call"
TODAY = "2026-06-12"

# ───────────────────────── shared chrome ─────────────────────────

NAV = """<header class="pnav">
  <a class="logo" href="/"><span class="logo__v">V</span>eblen</a>
  <nav class="pnav__links" aria-label="Primary">
    <a href="/tradie-marketing/"{c_tm}>Tradie Marketing</a>
    <a href="/services/websites/"{c_web}>Websites</a>
    <a href="/services/meta-ads/"{c_meta}>Meta Ads</a>
    <a href="/services/google-ads/"{c_g}>Google Ads</a>
    <a href="/case-studies/"{c_cs}>Results</a>
    <a href="/about/"{c_ab}>About</a>
  </nav>
  <a class="btn btn--solid" href="{book}">Book a call</a>
</header>"""

FOOTER = """<footer class="pfooter">
  <div class="pfooter__cols">
    <div>
      <p class="logo"><span class="logo__v">V</span>eblen</p>
      <p>The growth engine for Australian trade and service businesses that intend to own their market.</p>
    </div>
    <div>
      <p class="pfooter__h">Tradie marketing</p>
      <a href="/tradie-marketing/">Marketing for tradies</a>
      <a href="/tradie-marketing/gold-coast/">Gold Coast</a>
      <a href="/tradie-marketing/brisbane/">Brisbane</a>
      <a href="/case-studies/">Case studies</a>
    </div>
    <div>
      <p class="pfooter__h">Services</p>
      <a href="/services/websites/">Websites for tradies</a>
      <a href="/services/meta-ads/">Meta &amp; Facebook ads</a>
      <a href="/services/google-ads/">Google Ads</a>
      <a href="/services/crm-automation/">CRM &amp; automation</a>
      <a href="/services/seo/">SEO &amp; AI search</a>
      <a href="/services/cro/">Landing pages &amp; CRO</a>
    </div>
    <div>
      <p class="pfooter__h">Company</p>
      <a href="/about/">About Veblen</a>
      <a href="{book}">Book a strategy call</a>
      <a href="mailto:admin@veblengroup.com.au">admin@veblengroup.com.au</a>
      <a href="tel:+61468068886">+61 468 068 886</a>
    </div>
  </div>
  <p class="pfooter__legal">© 2026 Veblen Pty Ltd · Gold Coast, QLD · All rights reserved.</p>
</footer>"""

FORM = """<form class="pform" id="pform" data-entrypath="{entrypath}" novalidate>
  <div class="pform__row">
    <label>First name<input type="text" name="first_name" autocomplete="given-name" required /></label>
    <label>Last name<input type="text" name="last_name" autocomplete="family-name" required /></label>
  </div>
  <label>Business name<input type="text" name="business" autocomplete="organization" required /></label>
  <div class="pform__row">
    <label>Phone<input type="tel" name="phone" autocomplete="tel" required /></label>
    <label>Email<input type="email" name="email" autocomplete="email" required /></label>
  </div>
  <label>Annual revenue
    <select name="revenue" required>
      <option value="" selected disabled>Select revenue</option>
      <option value="under-500k">Under $500k</option>
      <option value="500k-1m">$500k – $1M</option>
      <option value="1m-3m">$1M – $3M</option>
      <option value="3m-10m">$3M – $10M</option>
      <option value="10m-plus">$10M+</option>
    </select>
  </label>
  <button class="btn btn--solid btn--lg" type="submit">{cta_label}</button>
  <p class="pform__success" id="pform-success" hidden>✓ Got it. We'll come back to you within one business day.</p>
</form>"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{meta}" />
  {robots}<link rel="canonical" href="{canonical}" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{meta}" />
  <meta property="og:image" content="{domain}/og-image.jpg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700;800&family=DM+Serif+Display:ital@1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" />
  <link rel="stylesheet" href="/css/pages.css?v=cd2" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-QXMKRXT694"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-QXMKRXT694');</script>
  <script type="application/ld+json">{jsonld}</script>
</head>
<body>
{nav}
<main>
{body}
<section class="pcta" id="contact">
  <div class="pcta__in">
    <div>
      <h2>{cta_h2}</h2>
      <p class="pcta__sub">{cta_sub}</p>
      <p class="pcta__alt">Prefer to talk it through? <a href="{book}">Book a 30-minute strategy call</a> — straight into Zac's calendar.</p>
    </div>
    {form}
  </div>
</section>
</main>
{footer}
<script src="/js/page.js?v=cd2" defer></script>
</body>
</html>"""

def jsonld_service(name, desc, path):
    return json.dumps([{
        "@context": "https://schema.org", "@type": "Service",
        "name": name, "description": desc,
        "provider": {"@type": "ProfessionalService", "name": "Veblen", "legalName": "Veblen Pty Ltd",
                     "url": DOMAIN, "telephone": "+61468068886", "email": "admin@veblengroup.com.au",
                     "address": {"@type": "PostalAddress", "addressLocality": "Gold Coast", "addressRegion": "QLD", "addressCountry": "AU"},
                     "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "16"}},
        "areaServed": ["Gold Coast", "Brisbane", "Australia"], "url": DOMAIN + path,
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": DOMAIN + path},
        ],
    }], separators=(",", ":"))

def proofbar(items):
    cells = "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in items)
    return f'<div class="proofbar">{cells}</div>'

def qa(items):
    blocks = "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    return f'<div class="qa">{blocks}</div>'

def cases_block(cards):
    out = ""
    for card in cards:
        client, big, txt = card[0], card[1], card[2]
        link = card[3] if len(card) > 3 else "/case-studies/"
        out += f'<article class="case"><p class="case__client">{client}</p><b>{big}</b><p>{txt}</p><a href="{link}">Read the full case study →</a></article>'
    return f'<div class="cases">{out}</div>'

def steps_block(items):
    out = ""
    for n, (h, p) in enumerate(items, 1):
        out += f'<div class="step" data-fade><span class="step__n">{n:02d}</span><div><h3>{h}</h3><p>{p}</p></div></div>'
    return f'<div class="steps">{out}</div>'

def fcards(items):
    out = ""
    for h, p in items:
        out += f'<article class="fcard" data-fade><h3>{h}</h3><p>{p}</p></article>'
    return f'<div class="fgrid">{out}</div>'

def revs(items):
    out = ""
    for name, txt in items:
        out += f'<article class="rev" data-fade><p class="rev__stars">★★★★★</p><p>{txt}</p><b>{name} · Google review</b></article>'
    return f'<div class="revstrip">{out}</div>'

# Approved claim bank — every number here is already public on the live
# homepage (films/reviews/proof panels) or vault-approved wording.
CASES = {
    "ntt":  ("NT Trailers · Manufacturing", "600", "leads a month at under $32 cost per lead. Full CRM build, automated follow-up, ads that keep getting sharper.", "/case-studies/nt-trailers/"),
    "lcmb": ("LCMB Group · Electrical &amp; Air", "100+", "qualified leads, every month. In March 2026 the account produced 254 leads at a $25.66 average cost per lead.", "/case-studies/lcmb/"),
    "adv":  ("ADV+ Painting · Trades", "$0→$50k", "monthly revenue. From no online presence to a full pipeline: ads, automations and missed-call recovery.", "/case-studies/adv-painting/"),
}
REV_LUKE = ("Luke Muir, LCMB Group", "Veblen completely transformed our lead flow. We went from chasing cold enquiries to having jobs booked automatically before a competitor even sees the notification.")
REV_JOSH = ("Josh Norris, NT Trailers", "600 leads a month at under $32 CPL. The team built out our entire CRM, automated follow-up sequences, and the ads keep getting sharper.")
REV_DAVID = ("David, ADV+ Painting", "We went from $0 to $50k a month in revenue — the system they built is genuinely incredible.")
REV_DAVIDA = ("David A.", "Missed call text-back was live within days of onboarding and we started converting jobs we used to lose. The team actually understands the trades.")

PAGES = []

# ───────────────────────── 1 · /tradie-marketing/ ─────────────────────────
PAGES.append(dict(
    path="/tradie-marketing/",
    nav_active="c_tm",
    title="Marketing for Tradies | Tradie Marketing Agency — Veblen, QLD",
    meta="Veblen is the tradie marketing agency behind LCMB, NT Trailers and ADV+ Painting. Ads, websites, CRM and AI follow-up that turn clicks into booked jobs. Gold Coast, Brisbane and Australia-wide.",
    entrypath="page-tradie-marketing",
    cta_label="Get my growth plan →",
    cta_h2="Ready to own your trade's market?",
    cta_sub="Sixty seconds. Tell us where the business is at and we'll show you exactly what the engine looks like for your trade.",
    jsonld=jsonld_service("Tradie Marketing", "Marketing for tradies: paid ads, websites, CRM automation and AI follow-up for Australian trade businesses.", "/tradie-marketing/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / Tradie marketing</p>
  <h1>Marketing for tradies that ends in <span class="hl">booked jobs</span>, not reports.</h1>
  <p class="phero__sub">Most agencies sell tradies clicks. We build the whole engine — <strong>ads, website, CRM and AI follow-up that answers every lead in under 60 seconds</strong> — because the first business to call wins the job. Built on the Gold Coast, proven across Australia.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my growth plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
    <span class="phero__note">No lock-in pitch. No pressure.</span>
  </div>
</section>
{proofbar([("600", "leads/mo — NT Trailers"), ("100+", "leads/mo — LCMB Group"), ("$0→$50k", "monthly revenue — ADV+ Painting"), ("5.0★", "16 Google reviews")])}
<section class="psec">
  <h2>Who is the best marketing agency for tradies?</h2>
  <div class="answer"><p>The right tradie marketing agency is the one that can show you trade clients, real lead numbers and the system that produced them. Veblen runs the growth engines behind LCMB Group (electrical &amp; air conditioning), NT Trailers (trailer manufacturing), ADV+ Painting, Streamline Plumbing and TTTM Construction — generating hundreds of qualified trade leads every month and answering every one of them in under 60 seconds.</p></div>
  <p class="lead">We're not generalists who happen to take trade clients. Trades are our home ground: we know what a qualified lead is worth on the tools, what a tyre-kicker looks like in a lead form, and why speed-to-lead decides who wins the job.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>The engine, not the pieces.</h2>
  <p class="lead">Every part feeds the next. That's the difference between buying ads and owning a market.</p>
  {fcards([
    ('<span class="n">01</span>Ads that pull real work', "Meta-first paid media backed by Google, aimed at the jobs you actually want — not whoever clicks cheapest. Creative shot on real sites with real teams."),
    ('<span class="n">02</span>A website built to convert', "Fast, mobile-first pages with one job: turn the visit into a phone call or a booked quote. See <a href='/services/websites/'>websites for tradies</a>."),
    ('<span class="n">03</span>CRM + automation', "Every lead lands in one pipeline, gets followed up automatically, and nothing falls through the cracks between site visits. See <a href='/services/crm-automation/'>CRM &amp; automation</a>."),
    ('<span class="n">04</span>AI follow-up in under 60 seconds', "Infrastructure our engineers build: the instant a lead comes in, it gets a response — before your competitor has even seen the notification."),
  ])}
</div></section>
<section class="psec">
  <h2>Proof from the tools.</h2>
  {cases_block([CASES["ntt"], CASES["lcmb"], CASES["adv"]])}
  {revs([REV_JOSH, REV_LUKE, REV_DAVIDA])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>How it works.</h2>
  {steps_block([
    ("Strategy call", "Thirty minutes. We look at your trade, your area, your capacity and your numbers — and tell you straight whether we can move them."),
    ("Engine build", "Ads, landing pages, CRM, automation and follow-up built as one system in the first weeks — not bolted together over a year."),
    ("Leads flow, jobs book", "Qualified enquiries land in your pipeline and get answered in under a minute, around the clock."),
    ("Scale what works", "Live attribution shows which ads produce booked jobs, not just clicks. We cut what doesn't and pour fuel on what does."),
  ])}
</div></section>
<section class="psec">
  <h2>Questions tradies actually ask us.</h2>
  {qa([
    ("How much does tradie marketing cost in Australia?", "Our partnership engine starts at $5,900/month plus ad spend, with most partners landing at $7,499/month. For businesses still building toward $1M revenue, Veblen Systems start from $600 — websites, video, ads setup and CRM builds delivered in days."),
    ("How many leads can a trade business expect from paid ads?", "It depends on trade, area and budget — but for scale reference: NT Trailers generates around 600 leads a month and LCMB Group 100+ qualified leads a month on our engine. On a strategy call we'll model your trade and suburb honestly rather than promise a number."),
    ("Do you only work with big trade businesses?", "No. The Partnership (from $5,900/mo) is built for businesses doing $1M+ a year. Under that, Veblen Systems gives you the same websites, ads and CRM infrastructure our million-dollar clients run, at a fixed price."),
    ("What trades do you work with?", "Electrical, air conditioning, plumbing, painting, construction, trailers and manufacturing, landscaping and more. If the job is won by whoever answers first with a fair quote, our engine fits."),
    ("Why does speed-to-lead matter so much for tradies?", "Because homeowners ring the next number the moment they hit voicemail. Our AI follow-up infrastructure responds to every enquiry in under 60 seconds, day or night — which is routinely the difference between winning and losing the job."),
    ("Do you lock clients into long contracts?", "Partnership tiers run on a three-month minimum because real growth takes longer than 30 days. After that, we keep the work by earning it — most of our trade clients have been with us for years."),
  ])}
</section>
""",
))

# ───────────────────────── 2 · gold coast ─────────────────────────
PAGES.append(dict(
    path="/tradie-marketing/gold-coast/",
    nav_active="c_tm",
    title="Marketing Agency Gold Coast for Tradies & Local Business | Veblen",
    meta="Gold Coast marketing agency specialising in tradies and local service businesses. Meta ads, Google Ads, websites and CRM with AI follow-up — 5.0★ across 16 Google reviews. Based here, proven here.",
    entrypath="page-tradie-marketing-gold-coast",
    cta_label="Talk to a Gold Coast team →",
    cta_h2="Own the Gold Coast in your trade.",
    cta_sub="We're local. We know what a lead from Robina costs versus one from Coomera. Tell us your trade and we'll map your suburb-by-suburb play.",
    jsonld=jsonld_service("Marketing Agency Gold Coast", "Gold Coast marketing agency for tradies and local service businesses: ads, websites, CRM and AI follow-up.", "/tradie-marketing/gold-coast/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / <a href="/tradie-marketing/">Tradie marketing</a> / Gold Coast</p>
  <h1>The Gold Coast marketing agency that <span class="hl">tradies</span> built their pipelines on.</h1>
  <p class="phero__sub">Veblen is headquartered on the Gold Coast, and our longest-running client relationships are GC trade businesses. <strong>Ads, websites, CRM and AI follow-up under 60 seconds</strong> — run by a team you can actually sit across a table from.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my Gold Coast plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("GC", "headquartered, since day one"), ("100+", "leads/mo — LCMB (GC & BNE)"), ("5.0★", "16 Google reviews · Gold Coast"), ("<60s", "AI lead response, every enquiry")])}
<section class="psec">
  <h2>Which marketing agency on the Gold Coast is best for trade businesses?</h2>
  <div class="answer"><p>For trade and local service businesses on the Gold Coast, Veblen is the agency with the deepest trade-specific track record: LCMB Group (electrical &amp; air conditioning across the Gold Coast and Brisbane) runs on our engine at 100+ qualified leads a month, alongside ADV+ Painting, Streamline Plumbing and TTTM Construction. We hold a 5.0-star rating across 16 Google reviews.</p></div>
  <p class="lead">Most GC agencies are generalists chasing whoever will sign. We specialise: trades and local services, where the maths is honest — a lead either becomes a booked job or it doesn't, and the engine gets judged on that.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>What we run for Gold Coast businesses.</h2>
  {fcards([
    ('<span class="n">01</span>Local lead generation', "Meta and Google campaigns tuned suburb by suburb — Southport to Coolangatta, and west to the growth corridors. See <a href='/services/meta-ads/'>Meta ads</a> and <a href='/services/google-ads/'>Google Ads</a>."),
    ('<span class="n">02</span>Websites that book jobs', "Mobile-first, loads in about a second, built to convert a GC homeowner standing in their kitchen with a problem. See <a href='/services/websites/'>websites</a>."),
    ('<span class="n">03</span>CRM + AI follow-up', "Every call, form and Facebook lead in one pipeline, answered in under 60 seconds — even when your crew is on the tools. See <a href='/services/crm-automation/'>CRM &amp; automation</a>."),
    ('<span class="n">04</span>Local search &amp; AI visibility', "Google Business Profile, reviews and the new layer most agencies ignore: being the business AI assistants recommend. See <a href='/services/seo/'>SEO &amp; AI search</a>."),
  ])}
</div></section>
<section class="psec">
  <h2>Gold Coast proof.</h2>
  {cases_block([CASES["lcmb"], CASES["adv"]])}
  {revs([REV_LUKE, ("Amanda A", "I recently had the pleasure of working with Veblen Group, and I must say, their professionalism and communication are outstanding."), ("Southport Tyres", "Best in the Business! So happy with the quality of work these guys produce. The attention to detail and creativity they bring is unmatched.")])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>Questions Gold Coast owners ask us.</h2>
  {qa([
    ("How much should a Gold Coast trade business spend on marketing?", "As a working rule: enough ad spend to feed your crew's capacity, plus an engine that converts it. Most of our GC partners run $2,000–$15,000/month in ad spend on top of the engine. On a call we'll model it for your trade rather than guess."),
    ("Do you work with businesses outside the trades?", "Yes — local service businesses with the same maths: real estate, clinics, automotive. Trades are the specialty, local service is the family."),
    ("Why use a local agency instead of a cheap offshore one?", "Because your market is here. We know GC suburbs, GC seasonality and GC buyers — and we put our own name on local results: 5.0 stars across 16 Google reviews from businesses you can ring."),
    ("Can you have something running fast?", "Yes. Veblen Systems (websites, ads setup, CRM builds, from $600) ship in days. Full partnership engines are live inside the first weeks."),
  ])}
</div></section>
""",
))

# ───────────────────────── 3 · brisbane ─────────────────────────
PAGES.append(dict(
    path="/tradie-marketing/brisbane/",
    nav_active="c_tm",
    title="Marketing Agency Brisbane for Tradies & Trade Businesses | Veblen",
    meta="Brisbane marketing agency for tradies and trade businesses. We run the lead engines behind Brisbane and SEQ trade companies — ads, websites, CRM, AI follow-up in under 60 seconds.",
    entrypath="page-tradie-marketing-brisbane",
    cta_label="Get my Brisbane plan →",
    cta_h2="Take the Brisbane market in your trade.",
    cta_sub="From Northside to Logan, the trade businesses winning Brisbane are the ones answering first. Tell us your trade — we'll show you the engine.",
    jsonld=jsonld_service("Marketing Agency Brisbane", "Brisbane marketing agency for tradies and trade businesses: ads, websites, CRM and AI follow-up.", "/tradie-marketing/brisbane/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / <a href="/tradie-marketing/">Tradie marketing</a> / Brisbane</p>
  <h1>A Brisbane marketing agency that talks in <span class="hl">booked jobs</span>.</h1>
  <p class="phero__sub">Veblen runs growth engines for trade businesses across Brisbane and South East Queensland — including LCMB Group's electrical and air conditioning operation spanning Brisbane and the Gold Coast. <strong>Ads, websites, CRM, and AI follow-up in under 60 seconds.</strong></p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my Brisbane plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("SEQ", "Brisbane + Gold Coast coverage"), ("100+", "leads/mo — LCMB (BNE & GC)"), ("600", "leads/mo — NT Trailers"), ("<60s", "AI lead response")])}
<section class="psec">
  <h2>Who should Brisbane trade businesses hire for marketing?</h2>
  <div class="answer"><p>Hire an agency that already runs profitable lead engines for trades in South East Queensland. Veblen's client engine generates 100+ qualified monthly leads for LCMB Group across Brisbane and the Gold Coast, and around 600 monthly leads for NT Trailers — with every enquiry answered by AI follow-up infrastructure in under 60 seconds.</p></div>
  <p class="lead">Brisbane is Australia's busiest trade market this decade — infrastructure pipelines, growth corridors and renovation demand all at once. The constraint isn't work. It's being the business that gets the call first.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>The Brisbane engine.</h2>
  {fcards([
    ('<span class="n">01</span>Lead generation that scales', "Meta-first campaigns with Google capture behind them, tuned to Brisbane's corridors — Northside, Southside, Ipswich, Logan, Moreton Bay. See <a href='/services/meta-ads/'>Meta ads</a>."),
    ('<span class="n">02</span>Websites built for one second', "Pages that load fast and convert Brisbane homeowners and builders into calls and quote requests. See <a href='/services/websites/'>websites for tradies</a>."),
    ('<span class="n">03</span>Pipeline you can trust', "CRM, automation and missed-call recovery so a lead from Chermside at 7pm doesn't die in a voicemail box. See <a href='/services/crm-automation/'>CRM &amp; automation</a>."),
    ('<span class="n">04</span>Own the search results', "Local SEO plus AI-search visibility, so you're the answer when Brisbane asks Google or ChatGPT who to call. See <a href='/services/seo/'>SEO &amp; AI search</a>."),
  ])}
</div></section>
<section class="psec">
  <h2>Proof across SEQ.</h2>
  {cases_block([CASES["lcmb"], CASES["ntt"], CASES["adv"]])}
  {revs([REV_JOSH, REV_LUKE])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>Brisbane questions, straight answers.</h2>
  {qa([
    ("Do you have Brisbane clients or just Gold Coast?", "Both. LCMB Group runs electrical and air conditioning across Brisbane and the Gold Coast on our engine, and our SEQ footprint spans trades from manufacturing to painting. We're an hour down the M1 and on site when it matters."),
    ("What does marketing cost for a Brisbane trade business?", "Partnership engines start at $5,900/month plus ad spend (most land at $7,499/month). Fixed-price systems — websites, ads setup, CRM builds — start around $600 for businesses still building toward $1M."),
    ("How fast can we see leads in Brisbane?", "Paid campaigns typically produce enquiries in the first days of going live. The bigger unlock is the follow-up engine behind them: answering every lead in under 60 seconds is routinely worth more than any single ad."),
    ("Can you handle a multi-crew, multi-suburb operation?", "Yes — that's exactly what the engine is for. Routing, pipelines per service line, and attribution that shows which suburb and which ad actually produced booked work."),
  ])}
</div></section>
""",
))

# ───────────────────────── 4 · websites ─────────────────────────
PAGES.append(dict(
    path="/services/websites/",
    nav_active="c_web",
    title="Websites for Tradies — Built in Days, Load in a Second | Veblen",
    meta="Websites for tradies that turn visits into booked jobs. Designed and built in days, load in about a second, wired into a CRM with AI follow-up. From $2,000. Gold Coast & Australia-wide.",
    entrypath="page-websites",
    cta_label="Get my website plan →",
    cta_h2="Your trade deserves better than a brochure.",
    cta_sub="Tell us your trade and what you've got now. We'll tell you straight what a site that books jobs looks like — and exactly what it costs.",
    jsonld=jsonld_service("Websites for Tradies", "Tradie website design: fast, conversion-built websites for trade businesses, wired into CRM and AI follow-up.", "/services/websites/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / Services / Websites</p>
  <h1>Websites for tradies that turn visits into <span class="hl">booked jobs</span>.</h1>
  <p class="phero__sub">A tradie website has one job: make the phone ring. We design and build <strong>fast, mobile-first sites in days — not months</strong> — and wire every form and call button into a CRM that follows up in under 60 seconds.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my website plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
    <span class="phero__note">5-Day Website from $2,000.</span>
  </div>
</section>
{proofbar([("7", "live client sites and counting"), ("~1s", "load target on every build"), ("5 days", "typical build, from $2,000"), ("<60s", "follow-up on every enquiry")])}
<section class="psec">
  <h2>What makes a good tradie website?</h2>
  <div class="answer"><p>A good tradie website loads in about a second on a phone, shows your trade, your area and your proof within one scroll, and makes calling or requesting a quote effortless. Behind the page, every enquiry should land in a CRM and get an instant response — because the homeowner who filled in your form is filling in your competitor's next. That's exactly how Veblen builds them.</p></div>
  <p class="lead">Most trade websites are digital brochures: pretty, slow, and silent on the one question a buyer has — <strong>"can these people fix my problem, here, soon?"</strong> We build conversion machines instead.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>What every Veblen build includes.</h2>
  {fcards([
    ('<span class="n">01</span>Built to convert', "One scroll to proof, one tap to call. Quote forms that ask only what's needed, click-to-call everywhere, and trust signals — reviews, photos of real jobs, real team."),
    ('<span class="n">02</span>Genuinely fast', "Static-first engineering, image discipline and zero bloat. About a second to load on a phone — because every extra second loses buyers."),
    ('<span class="n">03</span>Wired into the engine', "Forms land in a CRM pipeline, trigger AI follow-up in under 60 seconds and missed-call text-back. The site isn't the end of the funnel — it's the front door. See <a href='/services/crm-automation/'>CRM &amp; automation</a>."),
    ('<span class="n">04</span>Found on Google and beyond', "Clean technical SEO, suburb and service pages, schema, reviews — plus visibility in AI assistants, where buyers increasingly ask first. See <a href='/services/seo/'>SEO &amp; AI search</a>."),
  ])}
</div></section>
<section class="psec">
  <h2>Proof it works.</h2>
  {cases_block([CASES["adv"], CASES["lcmb"]])}
  {revs([REV_DAVID, ("Kyle Albert", "Zac was extremely professional and made the whole process easy. He explained everything clearly and the final product was absolutely incredible."), REV_DAVIDA])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>Tradie website questions.</h2>
  {qa([
    ("How much does a tradie website cost in Australia?", "Our 5-Day Website starts from $2,000 — designed, written, built and live. A full Business Launch System (website + socials + Google Business Profile) starts from $4,500. Partnership clients get landing pages and CRO as part of the engine."),
    ("How long does a tradie website take to build?", "Five days is our standard build. We can move that fast because we've built dozens of trade and local-service sites and know exactly what converts."),
    ("Will my website actually generate leads on its own?", "A website converts demand; it rarely creates it. That's why ours are built as the front door of a full engine — paid ads drive the right visitors, the site converts them, the CRM books them. Each part multiplies the others."),
    ("Can you rebuild my existing site without losing my Google rankings?", "Yes — redirects, metadata and structure are part of every rebuild, and speed improvements usually help rankings rather than hurt them."),
    ("Do I own the website?", "Yes. Your domain, your content, your site. No hostage hosting."),
  ])}
</div></section>
""",
))

# ───────────────────────── 5 · google ads ─────────────────────────
PAGES.append(dict(
    path="/services/google-ads/",
    nav_active="c_g",
    title="Google Ads for Tradies & Local Business — Gold Coast Agency | Veblen",
    meta="Google Ads management for tradies and local businesses. Search campaigns that capture buyers at the moment they need you, wired into AI follow-up. Gold Coast based, Australia-wide.",
    entrypath="page-google-ads",
    cta_label="Get my Google Ads plan →",
    cta_h2="Be the answer when they search.",
    cta_sub="Tell us your trade and your area. We'll tell you what the auction looks like, what a lead should cost, and whether Google is even your best first move.",
    jsonld=jsonld_service("Google Ads Management", "Google Ads management for trade and local service businesses across Australia.", "/services/google-ads/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / Services / Google Ads</p>
  <h1>Google Ads that capture buyers at the <span class="hl">exact moment</span> they need you.</h1>
  <p class="phero__sub">When the hot water dies or the switchboard trips, someone searches — and the business at the top of that search gets the call. We run <strong>tight, capacity-matched Google Ads</strong> for trades and local services, wired straight into AI follow-up under 60 seconds.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my Google Ads plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("Search-first", "no junk display spend"), ("$0→$50k", "ADV+ Painting, ads + engine"), ("100%", "call + form tracking on every campaign"), ("<60s", "lead response, every enquiry")])}
<section class="psec">
  <h2>Are Google Ads worth it for tradies?</h2>
  <div class="answer"><p>Yes — when three things are true: the campaign only targets searches with buying intent, every call and form is tracked to a booked job (not just a click), and every lead is answered fast. Run that way, Google Ads is the highest-intent lead source a trade business can buy: ADV+ Painting went from no online presence to $50k months with Google Ads as a core channel of their Veblen engine.</p></div>
  <p class="lead">Run badly — broad keywords, no negatives, leads ringing out — Google Ads is the fastest way to burn a budget. The auction doesn't forgive sloppiness. That's the whole reason to have it run by people who live in it.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>How we run Google for trades.</h2>
  {fcards([
    ('<span class="n">01</span>Intent only', "Exact and phrase match on searches that mean money in your trade, with aggressive negative lists. No display remnants, no spray-and-pray."),
    ('<span class="n">02</span>Landing pages that match', "Ads land on pages built for the search, not your homepage — message match is half the conversion rate. See <a href='/services/cro/'>landing pages &amp; CRO</a>."),
    ('<span class="n">03</span>Tracking to booked jobs', "Calls, forms and bookings tracked through the CRM so budget decisions are made on jobs won, not clicks bought."),
    ('<span class="n">04</span>Meta + Google together', "Google captures demand; Meta creates it. The businesses that own their market run both in one engine. See <a href='/services/meta-ads/'>Meta ads</a>."),
  ])}
</div></section>
<section class="psec">
  <h2>Proof.</h2>
  {cases_block([CASES["adv"], CASES["lcmb"]])}
  {revs([REV_DAVID, REV_LUKE])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>Google Ads questions.</h2>
  {qa([
    ("How much should a tradie spend on Google Ads?", "Enough to matter in your auction, not a dollar more than your crew can service. For most trades that's $1,500–$10,000/month depending on area and competition. We size it on a call against your capacity and the real CPCs in your trade."),
    ("What does a lead from Google Ads cost for a trade business?", "It varies hard by trade — emergency trades pay more per click but convert at much higher rates. We'll show you the live auction numbers for your trade and suburb on a strategy call rather than quote a fantasy average."),
    ("Google Ads or Facebook ads for a tradie — which first?", "Google captures people already searching for your trade; Meta creates demand and builds your name. Urgent-need trades usually start Google-first; consideration purchases lean Meta-first. The full answer depends on your trade, and we'll give it to you straight."),
    ("Do you lock me into a contract for ad management?", "Partnership engines run a three-month minimum — long enough for the data to compound. Ads Ignition, our campaign setup, starts from $600 one-off if you want it built right and run it yourself."),
  ])}
</div></section>
""",
))

# ───────────────────────── 6 · meta ads ─────────────────────────
PAGES.append(dict(
    path="/services/meta-ads/",
    nav_active="c_meta",
    title="Facebook & Meta Ads for Tradies — Lead Generation | Veblen",
    meta="Meta and Facebook ads for tradies and local businesses. The engine behind 600 leads/month at NT Trailers and 254 leads in a month at LCMB. Creative shot on real job sites, leads answered in under 60 seconds.",
    entrypath="page-meta-ads",
    cta_label="Get my Meta ads plan →",
    cta_h2="Fill the pipeline before they even search.",
    cta_sub="Tell us your trade and your monthly capacity. We'll model what Meta can produce for you — with numbers from trades we already run.",
    jsonld=jsonld_service("Meta & Facebook Ads", "Meta and Facebook advertising for trade and local service businesses across Australia.", "/services/meta-ads/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / Services / Meta ads</p>
  <h1>Meta ads are our <span class="hl">home ground</span>.</h1>
  <p class="phero__sub">Meta-first is how our biggest client results happened: <strong>600 leads a month at NT Trailers, 100+ a month at LCMB</strong>. Scroll-stopping creative shot on real job sites, lead forms tuned for quality, and every enquiry answered in under 60 seconds.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my Meta ads plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("600", "leads/mo — NT Trailers"), ("254", "leads in March 2026 — LCMB account"), ("$25.66", "average CPL on that account that month"), ("<60s", "AI response on every lead")])}
<section class="psec">
  <h2>Do Facebook ads work for tradies?</h2>
  <div class="answer"><p>Yes — Meta is the most scalable lead source for most trade businesses, because it reaches homeowners before they search. The proof on our engine: NT Trailers generates around 600 leads a month at under $32 cost per lead, and LCMB Group's account produced 254 leads in March 2026 at a $25.66 average cost per lead. The catch: Meta leads must be answered within minutes or they go cold — which is why our engine answers every one in under 60 seconds.</p></div>
  <p class="lead">Meta rewards two things ruthlessly: <strong>creative that stops the scroll</strong> and <strong>speed of follow-up</strong>. We're built around both — on-site shoots, an in-house creative engine, and follow-up infrastructure our engineers run.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>Why our Meta engine wins.</h2>
  {fcards([
    ('<span class="n">01</span>Creative that makes the market look', "Real crews, real jobs, real owners on camera. Our creative team is the sharpest weapon we have — and the reviews say the same."),
    ('<span class="n">02</span>Lead quality, engineered', "High-intent lead forms with qualifying questions, audience strategy per trade, and relentless pruning of what produces tyre-kickers."),
    ('<span class="n">03</span>Follow-up under 60 seconds', "A Meta lead answered in a minute books; the same lead answered at 5pm doesn't. AI follow-up infrastructure answers instantly, every time."),
    ('<span class="n">04</span>Judged on booked jobs', "CRM-tracked attribution from ad to revenue. We pause by performance, scale by performance, and report in dollars — not impressions."),
  ])}
</div></section>
<section class="psec">
  <h2>The receipts.</h2>
  {cases_block([CASES["ntt"], CASES["lcmb"], CASES["adv"]])}
  {revs([REV_JOSH, REV_LUKE])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>Meta ads questions.</h2>
  {qa([
    ("How much do Facebook leads cost for trade businesses?", "On our engine, real examples: NT Trailers averages under $32 per lead at 600 leads/month scale; LCMB's account averaged $25.66 per lead across 254 leads in March 2026. Your trade and area will differ — we model it honestly on a call."),
    ("What budget do I need to start with Meta ads?", "Most trade partners run $2,000–$15,000/month in ad spend. Below around $1,500/month, Meta struggles to exit learning in most trade auctions — we'll tell you if your budget isn't ready rather than take it."),
    ("Why do Facebook leads have a bad reputation with tradies?", "Because most businesses answer them hours later. Meta leads are interrupt-driven — the prospect wasn't searching, so interest decays in minutes. Answered in under 60 seconds with a qualifying flow, they book. That follow-up engine is half of what you're buying."),
    ("Who owns the ad account and the creative?", "You do. Your ad account, your page, your footage. We build the engine in your house, not ours."),
  ])}
</div></section>
""",
))

# ───────────────────────── 7 · crm automation ─────────────────────────
PAGES.append(dict(
    path="/services/crm-automation/",
    nav_active="",
    title="CRM for Tradies — Setup, Automation & AI Follow-Up | Veblen",
    meta="CRM setup and automation for tradies and local businesses. One pipeline for every lead, missed-call text-back, and AI follow-up in under 60 seconds. Built from $797 fixed.",
    entrypath="page-crm-automation",
    cta_label="Get my CRM plan →",
    cta_h2="Stop losing jobs you already paid to find.",
    cta_sub="Tell us how leads reach you today — calls, forms, Facebook, word of mouth. We'll show you where they're leaking and the system that catches them.",
    jsonld=jsonld_service("CRM Setup & Automation", "CRM builds, automation and AI follow-up for trade and local service businesses.", "/services/crm-automation/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / Services / CRM &amp; automation</p>
  <h1>Every lead. One pipeline. <span class="hl">Answered in 60 seconds.</span></h1>
  <p class="phero__sub">The most expensive lead is the one you already paid for and never called back. We build <strong>CRM systems for trade businesses</strong> — every call, form and Facebook lead in one pipeline, with automated follow-up that never sleeps and never forgets.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my CRM plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
    <span class="phero__note">CRM builds from $797 fixed.</span>
  </div>
</section>
{proofbar([("1", "pipeline for every lead source"), ("<60s", "AI response to new enquiries"), ("24/7", "missed-call text-back"), ("$797", "fixed-price CRM build, from")])}
<section class="psec">
  <h2>Does a tradie really need a CRM?</h2>
  <div class="answer"><p>If you get more than a few enquiries a week, yes. A CRM for a trade business is the difference between leads living in one pipeline with automatic follow-up, and leads dying in voicemail, text threads and a glovebox notebook. The day-one win is usually missed-call text-back: one client had it live within days of onboarding and immediately started converting jobs that used to ring out.</p></div>
  <p class="lead">Our position is simple: <strong>follow-up is infrastructure, not willpower.</strong> Nobody runs a crew all day and reliably calls every lead back at night. The system has to do it.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>What we build.</h2>
  {fcards([
    ('<span class="n">01</span>One pipeline, every source', "Phone, website forms, Facebook lead forms, Google — everything lands in one board your team actually uses, staged from new lead to booked job."),
    ('<span class="n">02</span>AI follow-up under 60 seconds', "Engineered infrastructure that responds to every new enquiry instantly, qualifies politely, and pushes for the booking — then hands a warm one to a human."),
    ('<span class="n">03</span>Missed-call text-back', "Crew on the tools, phone rings out, customer instantly gets a text that keeps the job alive. The single highest-ROI automation in the trades."),
    ('<span class="n">04</span>Reviews + repeat work on autopilot', "Post-job review requests, seasonal re-engagement, quote chase sequences. The database you already own becomes a revenue channel."),
  ])}
</div></section>
<section class="psec">
  <h2>What it does to a business.</h2>
  {cases_block([CASES["ntt"], CASES["adv"]])}
  {revs([REV_DAVIDA, REV_JOSH])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>CRM questions.</h2>
  {qa([
    ("What does a CRM setup cost for a trade business?", "Our CRM build starts from $797 — pipeline, lead capture wiring, missed-call text-back and core automations, delivered in days. Full AI follow-up engines come with partnership tiers from $5,900/month."),
    ("What's the best CRM for tradies?", "The one your team actually uses, wired to answer leads instantly. We build on proven platforms rather than locking you into something exotic — and you keep ownership of the account and your data."),
    ("Will my team actually use it?", "That's a build problem, not a willpower problem. We set it up around how your business already runs — stages that match your real workflow, automations that remove admin instead of adding it — and train your team on go-live."),
    ("Can it work with my existing job management software?", "Usually, yes. The CRM handles the front of house (leads, follow-up, bookings) and connects to job management for the back. We map your stack on the call."),
  ])}
</div></section>
""",
))

# ───────────────────────── 8 · seo / aeo ─────────────────────────
PAGES.append(dict(
    path="/services/seo/",
    nav_active="",
    title="SEO for Tradies + AI Search Visibility (AEO) | Veblen",
    meta="SEO for tradies that wins Google — and the AI layer most agencies ignore: being the business ChatGPT and Google's AI recommend. Local SEO, content, reviews and entity work, tracked monthly.",
    entrypath="page-seo",
    cta_label="Get my search plan →",
    cta_h2="Be the answer — on Google and in AI.",
    cta_sub="Tell us your trade and area, and we'll baseline where you rank today: Google, the map pack, and what the AI assistants say when someone asks who to call.",
    jsonld=jsonld_service("SEO & AI Search Optimisation", "Local SEO and AI search (AEO) visibility for trade and local service businesses.", "/services/seo/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / Services / SEO &amp; AI search</p>
  <h1>Rank where buyers ask — <span class="hl">Google and AI.</span></h1>
  <p class="phero__sub">Search changed. Buyers still Google your trade — but a growing share now ask ChatGPT and Google's AI who to call, and those answers cite businesses with real proof. We run <strong>SEO for trade businesses plus the AI-visibility layer (AEO)</strong> most agencies haven't even heard of.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my search plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("Local-first", "map pack + suburb pages"), ("AEO", "AI-answer visibility, tracked monthly"), ("0", "fake-review shortcuts, ever"), ("Monthly", "rank + AI-mention reporting")])}
<section class="psec">
  <h2>Is SEO worth it for a trade business?</h2>
  <div class="answer"><p>Yes — with the right expectations. For tradies, SEO is a compounding asset: the Google Business Profile and map pack drive calls within months, suburb and service pages build durable rankings over six to twelve, and the same work now feeds a third channel — AI assistants, which recommend businesses with consistent reviews, real proof and clean structured data. Paid ads buy this month's pipeline; search owns next year's.</p></div>
  <p class="lead">We practice what we sell: this site runs the exact playbook — structured data, answer-first content, entity work, AI-crawler access — and we track our own AI mentions the same way we'd track yours.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>The full search stack.</h2>
  {fcards([
    ('<span class="n">01</span>Local SEO that rings phones', "Google Business Profile optimisation, review velocity (earned, never gated), citations and the map pack — where trade buying decisions actually happen."),
    ('<span class="n">02</span>Pages that earn rankings', "Service and suburb pages with genuinely local content and proof — built on a fast site, because speed is a ranking input. See <a href='/services/websites/'>websites</a>."),
    ('<span class="n">03</span>AEO — the AI answer layer', "Structured data, entity consistency, answer-first content and AI-crawler access, so assistants can find, trust and recommend you. Tracked with monthly AI-mention reports."),
    ('<span class="n">04</span>Authority that compounds', "Real case studies, real numbers and local press — the citations both Google and AI models weight most."),
  ])}
</div></section>
<section class="psec">
  <h2>Why trust us with search?</h2>
  {cases_block([CASES["lcmb"], CASES["adv"]])}
  {revs([REV_LUKE, ("Jared Kalischer", "If you're looking for elite-level marketing that actually delivers results, look no further. The team is world-class and the work they produce is genuinely exceptional.")])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>SEO &amp; AEO questions.</h2>
  {qa([
    ("How long does SEO take for a tradie?", "Map-pack and Google Business Profile improvements typically show in weeks. Competitive suburb and service rankings take three to twelve months depending on your market. Anyone promising page one in 30 days is selling you something that will eventually hurt you."),
    ("What is AEO and do I actually need it?", "Answer Engine Optimisation — being visible when buyers ask AI assistants instead of Googling. It's earned the same way trust is: consistent reviews, real proof, structured data and content that answers questions directly. It's early — which is exactly why moving now is cheap and moving late will be expensive."),
    ("Can you guarantee #1 on Google?", "No honest agency can — Google itself says so. What we guarantee is the playbook executed properly, your numbers reported monthly without spin, and the same system we use on our own brand."),
    ("Do reviews really affect SEO?", "Heavily — for the map pack and for AI answers. We build review velocity into the engine: earned, compliant, never gated or incentivised."),
  ])}
</div></section>
""",
))

# ───────────────────────── 9 · cro ─────────────────────────
PAGES.append(dict(
    path="/services/cro/",
    nav_active="",
    title="Landing Pages & CRO for Trade Businesses | Veblen",
    meta="Landing pages and conversion rate optimisation for tradies. Every Veblen page must pass a 10-point conversion standard before a dollar of ad spend touches it. Same system, available for your business.",
    entrypath="page-cro",
    cta_label="Get my conversion audit →",
    cta_h2="Your ads are fine. Your page is the leak.",
    cta_sub="Send us the page your ads land on. We'll run it through the same 10-point standard we gate our own pages with, and show you the fixes in priority order.",
    jsonld=jsonld_service("Landing Pages & CRO", "Landing page builds and conversion rate optimisation for trade and local service businesses.", "/services/cro/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / Services / Landing pages &amp; CRO</p>
  <h1>Double the bookings without spending <span class="hl">another dollar</span> on ads.</h1>
  <p class="phero__sub">Most trade businesses don't have a traffic problem — they have a conversion problem. We build and optimise <strong>landing pages that turn paid clicks into booked jobs</strong>, gated by the same 10-point standard every page we run our own money through must pass.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my conversion audit</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("10-pt", "standard every page must pass"), ("~1s", "load target, every build"), ("1:1", "message match, ad to page"), ("A/B", "tested, not guessed")])}
<section class="psec">
  <h2>What is CRO and why should a tradie care?</h2>
  <div class="answer"><p>Conversion rate optimisation is the discipline of getting more booked jobs from the same traffic. If 100 clicks currently produce 3 enquiries and the page is rebuilt to produce 6, your cost per lead just halved without touching the ad account. For trade businesses spending real money on ads, page conversion is usually the single highest-leverage fix available — and the most neglected.</p></div>
  <p class="lead">We hold our own work to this: <strong>no Veblen campaign sends paid traffic to a page that hasn't passed our 10-point Great Page Standard.</strong> Message match, one clear action, proof above the fold, ~1-second load, mobile-first. The same gate is available for your pages.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>How we lift conversion.</h2>
  {steps_block([
    ("Audit against the standard", "Your page, scored against the 10-point gate: headline match, proof, friction, speed, mobile experience, trust signals. You get the scorecard and the priority list."),
    ("Rebuild what's broken", "Sometimes it's the form, sometimes the headline, sometimes the whole page. We fix in priority order — biggest conversion lever first."),
    ("Match every ad to its page", "Each campaign lands on a page that continues the exact promise of the ad that was clicked. Message match alone routinely moves conversion more than any redesign."),
    ("Test, measure, compound", "A/B tests on the levers that matter, judged on booked jobs through the CRM — not on opinions about colours."),
  ])}
</div></section>
<section class="psec">
  <h2>The engine it plugs into.</h2>
  {cases_block([CASES["adv"], CASES["ntt"]])}
  {revs([REV_DAVID, REV_JOSH])}
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>CRO questions.</h2>
  {qa([
    ("What's a good conversion rate for a tradie landing page?", "Paid-traffic landing pages for trades should convert at 5% or better — that's the floor we hold our own pages to. Many trade sites convert at 1–2%, which means more than half the achievable bookings are being left on the table."),
    ("Do I need a landing page, or can ads go to my homepage?", "Ads to a homepage is the most common money leak in trade marketing. A homepage speaks to everyone; a landing page continues the one promise the visitor just clicked. Dedicated pages per campaign almost always win."),
    ("How fast do CRO changes show results?", "Fast — conversion fixes apply to all existing traffic immediately. Meaningful read-outs typically take a few hundred clicks per variant, so higher-traffic accounts learn faster."),
    ("Is this included in your marketing partnerships?", "Yes — landing pages and CRO are built into Growth tier and above, because we refuse to scale ad spend into weak pages. It's also available standalone for businesses running their own ads."),
  ])}
</div></section>
""",
))

# ───────────────────────── 10 · case studies ─────────────────────────
PAGES.append(dict(
    path="/case-studies/",
    nav_active="c_cs",
    title="Tradie Marketing Case Studies & Results | Veblen",
    meta="Real results from real trade businesses: 600 leads/month at NT Trailers, 100+ monthly leads at LCMB Group, $0 to $50k months at ADV+ Painting. Numbers, methods and owner testimonials.",
    entrypath="page-case-studies",
    cta_label="Get results like these →",
    cta_h2="Your trade could be the next case study.",
    cta_sub="Every engine on this page started with one strategy call. Tell us where your business is at — we'll tell you honestly what's possible.",
    jsonld=jsonld_service("Case Studies", "Marketing case studies and results for Australian trade businesses.", "/case-studies/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / Case studies</p>
  <h1>Real trades. Real numbers. <span class="hl">No actors.</span></h1>
  <p class="phero__sub">Every number on this page comes from a client account we run, and every quote from a <strong>real owner on camera or on Google</strong>. This is what the engine does when it's installed properly.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Start your engine</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("600", "leads/mo — NT Trailers"), ("254", "leads in March 2026 — LCMB"), ("$0→$50k", "monthly revenue — ADV+"), ("5.0★", "16 Google reviews")])}
<section class="psec">
  <h2>NT Trailers — 600 leads a month, manufacturing at scale.</h2>
  <p class="lead"><a href='/case-studies/nt-trailers/' style='color:var(--orange)'>Read the full NT Trailers case study →</a></p>
  <p class="lead">Trailer manufacturing, Darwin. The engine: Meta-first campaigns with creative built around the product, full CRM build, and automated follow-up sequences. The result in Josh's words: <strong>"600 leads a month at under $32 CPL… NT Trailers has never had a pipeline this full."</strong> The deeper win is the system behind the ads — every lead followed up automatically, deposits nurtured, nothing leaking.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>LCMB Group — 100+ qualified leads, every month.</h2>
  <p class="lead"><a href='/case-studies/lcmb/' style='color:var(--orange)'>Read the full LCMB case study →</a></p>
  <p class="lead">Electrical and air conditioning across the Gold Coast and Brisbane. Meta-first lead generation with high-intent forms, CRM pipeline and AI follow-up in under 60 seconds. In March 2026 the account produced <strong>254 leads at a $25.66 average cost per lead</strong>. Luke's words: <strong>"jobs booked automatically before a competitor even sees the notification."</strong></p>
</div></section>
<section class="psec">
  <h2>ADV+ Painting — $0 to $50k months.</h2>
  <p class="lead"><a href='/case-studies/adv-painting/' style='color:var(--orange)'>Read the full ADV+ case study →</a></p>
  <p class="lead">Started from effectively zero online presence. The engine: Google Ads capturing search demand, website built to convert, automations and missed-call recovery catching every enquiry. David's words: <strong>"We went from $0 to $50k a month in revenue — the system they built is genuinely incredible."</strong></p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>And the ones beside them.</h2>
  <p class="lead">Streamline Plumbing. TTTM Construction. Fleck Group. Crown Realty. The pattern repeats because the engine repeats: <strong>ads → creative → website → CRM → AI follow-up → booked jobs.</strong></p>
  {revs([REV_JOSH, REV_LUKE, REV_DAVID, REV_DAVIDA])}
</div></section>
""",
))

# ───────────────────────── 11 · about ─────────────────────────
PAGES.append(dict(
    path="/about/",
    nav_active="c_ab",
    title="About Veblen — The Growth Engine Behind Australian Trades",
    meta="Veblen is a Gold Coast-based growth engine for Australian trade and service businesses — ads, creative, websites, CRM and AI infrastructure, run by the team that uses it on their own brand first.",
    entrypath="page-about",
    cta_label="Talk to the team →",
    cta_h2="We run our own playbook first.",
    cta_sub="The site you're on, the rankings it earns, the speed it loads at, the system that answers this form in under a minute — all of it is the product. Try us.",
    jsonld=json.dumps([{
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "Veblen", "legalName": "Veblen Pty Ltd", "url": DOMAIN,
        "telephone": "+61468068886", "email": "admin@veblengroup.com.au",
        "founder": {"@type": "Person", "name": "Zac Macanelly"},
        "address": {"@type": "PostalAddress", "addressLocality": "Gold Coast", "addressRegion": "QLD", "addressCountry": "AU"},
        "areaServed": ["Gold Coast", "Brisbane", "Australia"],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "16"},
        "sameAs": ["https://www.instagram.com/veblengrp", "https://www.linkedin.com/company/veblen-group", "https://www.tiktok.com/@veblengroup"],
    }], separators=(",", ":")),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / About</p>
  <h1>Not an agency. <span class="hl">A growth engine.</span></h1>
  <p class="phero__sub">Veblen exists because trade businesses kept getting sold marketing pieces — a logo here, some ads there, a website that never rings. We build the <strong>whole engine</strong>: ads, creative, website, CRM and AI follow-up infrastructure, engineered to work as one system.</p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="{BOOK_URL}">Book a call with Zac</a>
    <a class="btn btn--ghost" href="/case-studies/">See the results</a>
  </div>
</section>
{proofbar([("GC", "born and headquartered"), ("5.0★", "16 Google reviews"), ("6+", "trade verticals served"), ("<60s", "our own leads get answered too")])}
<section class="psec">
  <h2>What makes Veblen different?</h2>
  <div class="answer"><p>Three things. We specialise in trades and local services instead of taking anyone with a budget. We build complete engines — ads, creative, website, CRM, AI follow-up — instead of selling disconnected pieces. And we run every system on our own brand before selling it: the page you're reading is built on our own conversion standard, ranks by our own SEO playbook, and the form below answers you with the same under-60-second infrastructure our clients buy.</p></div>
  <p class="lead">Founded and led by <strong>Zac Macanelly</strong> on the Gold Coast. In-house strategy, on-site creative shoots, and a full production engine behind every account. AI does not replace the work — it's premium infrastructure our engineers build so the work never sleeps.</p>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>What we believe.</h2>
  {fcards([
    ('<span class="n">01</span>Judged in booked jobs', "Impressions, reach and pretty dashboards are exhaust. The engine is measured where it matters: jobs on the board, revenue in the account."),
    ('<span class="n">02</span>Speed wins trades', "The first business to answer wins the job. Everything we build serves speed — one-second pages, instant follow-up, same-week builds."),
    ('<span class="n">03</span>Proof over promises', "Every claim we publish is sourced from an account we run or an owner on the record. If we can't prove a number, it doesn't print."),
    ('<span class="n">04</span>Own it, never rent it', "Your ad account, your site, your data, your CRM. We build engines in your house — clients stay because it works, not because they're trapped."),
  ])}
</div></section>
<section class="psec">
  <h2>The owners we answer to.</h2>
  {revs([REV_LUKE, REV_JOSH, REV_DAVID, ("Amanda A", "Their professionalism and communication are outstanding. Highly recommend them to anyone looking for a quality marketing partner.")])}
</section>
""",
))


# ───────────────────────── 12 · case study: LCMB ─────────────────────────
PAGES.append(dict(
    path="/case-studies/lcmb/",
    nav_active="c_cs",
    title="LCMB Group Case Study — 100+ Tradie Leads a Month | Veblen",
    meta="How LCMB Group (electrical & air conditioning, Gold Coast + Brisbane) books 100+ qualified leads a month on the Veblen engine — including 254 leads at $25.66 average CPL in March 2026.",
    entrypath="page-case-lcmb",
    cta_label="Get results like LCMB →",
    cta_h2="Want this engine in your trade?",
    cta_sub="LCMB's engine took weeks to install, not months. Tell us your trade and area and we'll map the same system onto your business.",
    jsonld=jsonld_service("LCMB Group Case Study", "Marketing case study: 100+ qualified monthly leads for an electrical and air conditioning business across Gold Coast and Brisbane.", "/case-studies/lcmb/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / <a href="/case-studies/">Case studies</a> / LCMB Group</p>
  <h1>How LCMB Group books <span class="hl">100+ qualified leads</span> a month. Every month.</h1>
  <p class="phero__sub"><strong>Electrical &amp; air conditioning · Gold Coast + Brisbane · Veblen partner</strong></p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my growth plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("100+", "qualified leads, every month"), ("254", "leads in March 2026, account-wide"), ("$25.66", "average CPL that month"), ("<60s", "every lead answered")])}
<section class="psec">
  <h2>The 30-second version.</h2>
  <div class="answer"><p>LCMB Group is an electrical and air conditioning business operating across the Gold Coast and Brisbane. On the Veblen engine — Meta-first lead generation with high-intent forms, a CRM pipeline, and AI follow-up that answers every enquiry in under 60 seconds — the business books 100+ qualified leads month after month. In March 2026, the account produced 254 leads at a $25.66 average cost per lead.</p></div>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>The situation.</h2>
  <p class="lead">LCMB runs multiple service lines across two cities. The work was never the problem. <strong>Consistency was:</strong> lead flow that surged and died with referrals, and enquiries going cold in voicemail while the team was on the tools. For a multi-crew operation, inconsistent leads means crews you can never confidently keep busy.</p>
  <h2 style="margin-top:2.6rem">What we built.</h2>
  {steps_block([
    ("Meta-first lead generation", "Campaigns built per service line, with creative shot on real LCMB jobs — real crews, real installs, no stock footage. High-intent lead forms with qualifying questions filter tyre-kickers before they cost a phone call."),
    ("One pipeline for every lead", "Every enquiry — Meta, website, phone — lands in a single CRM pipeline staged from new lead to booked job, visible to the whole team."),
    ("AI follow-up in under 60 seconds", "The moment a lead arrives, the system responds — qualifies, answers questions, pushes for the booking. Luke's words: jobs get booked before a competitor has even seen the notification."),
    ("Performance-led optimisation", "Ads are paused and scaled on live cost-per-lead and booked-job data, not age or gut feel. The engine compounds because decisions follow the numbers."),
  ])}
</div></section>
<section class="psec">
  <h2>The results.</h2>
  <p class="lead"><strong>100+ qualified leads a month, sustained</strong> — not a spike month cherry-picked for a case study. The high-water proof: <strong>March 2026, 254 leads across the account at a $25.66 average cost per lead.</strong> Behind the volume, the speed: every enquiry answered in under 60 seconds, around the clock.</p>
  {revs([REV_LUKE])}
  <p class="lead" style="margin-top:1.6rem"><strong>What made the difference:</strong> not one tactic — the compounding of qualified lead flow and instant follow-up. Volume without speed leaks; speed without volume starves. The engine runs both.</p>
</section>

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
""",
))

# ───────────────────────── 13 · case study: NT Trailers ─────────────────────────
PAGES.append(dict(
    path="/case-studies/nt-trailers/",
    nav_active="c_cs",
    title="NT Trailers Case Study — 600 Leads a Month at Under $32 CPL | Veblen",
    meta="How NT Trailers generates around 600 leads a month at under $32 cost per lead on the Veblen engine — Meta-first campaigns, full CRM build and automated follow-up for a trailer manufacturer.",
    entrypath="page-case-nt-trailers",
    cta_label="Get results like NTT →",
    cta_h2="Manufacturing or high-ticket trade?",
    cta_sub="NTT's engine is built for considered purchases — nurture that holds buyers from first click to deposit. Tell us what you sell and we'll map it.",
    jsonld=jsonld_service("NT Trailers Case Study", "Marketing case study: around 600 monthly leads at under $32 CPL for an Australian trailer manufacturer.", "/case-studies/nt-trailers/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / <a href="/case-studies/">Case studies</a> / NT Trailers</p>
  <h1><span class="hl">600 leads a month</span> for a trailer manufacturer.</h1>
  <p class="phero__sub"><strong>Trailer manufacturing · Darwin, NT · Veblen partner</strong></p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my growth plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("600", "leads a month, at scale"), ("<$32", "cost per lead at that volume"), ("Full", "CRM build + automated follow-up"), ("Fullest", "pipeline in company history")])}
<section class="psec">
  <h2>The 30-second version.</h2>
  <div class="answer"><p>NT Trailers is a trailer manufacturer selling a considered, high-ticket product from Darwin. On the Veblen engine — Meta-first campaigns built around the product, a complete CRM build, and automated follow-up sequences — the business generates around 600 leads a month at under $32 cost per lead. In the owner's words: "NT Trailers has never had a pipeline this full."</p></div>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>The situation.</h2>
  <p class="lead">A trailer is not an impulse buy. Buyers compare, disappear, and come back weeks later — or never. Volume advertising alone produces enquiries that evaporate. The challenge: <strong>generate serious volume AND hold every buyer through a long consideration window</strong> without the sales team drowning in manual chasing.</p>
  <h2 style="margin-top:2.6rem">What we built.</h2>
  {steps_block([
    ("Product-first Meta campaigns", "Creative built around the trailers themselves — the builds, the specs, the real thing leaving the yard. At 600 leads a month, creative is a production line, not a one-off shoot."),
    ("Complete CRM build", "Every lead captured, staged and visible. A pipeline built for a considered purchase: enquiry, qualification, quote, deposit."),
    ("Automated follow-up sequences", "Instant first response, then structured nurture that keeps NT Trailers in front of the buyer through the comparison weeks — and chases quotes toward deposit without a human needing to remember."),
    ("Sharpen, relentlessly", "Josh's words: the ads keep getting sharper. Audiences, creative and forms iterated on live CPL — which is how 600 a month stays under $32."),
  ])}
</div></section>
<section class="psec">
  <h2>The results.</h2>
  <p class="lead"><strong>Around 600 leads a month at under $32 cost per lead</strong> — volume most manufacturers never see, at a CPL most can't hold at a tenth of the scale. The fullest pipeline in the company's history, with follow-up running on rails instead of memory.</p>
  {revs([REV_JOSH])}
  <p class="lead" style="margin-top:1.6rem"><strong>What made the difference:</strong> treating follow-up as infrastructure. At high-ticket price points the money isn't in the click — it's in the weeks after it. The CRM and nurture sequences are why volume became deposits instead of a full inbox.</p>
</section>

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
""",
))

# ───────────────────────── 14 · case study: ADV+ Painting ─────────────────────────
PAGES.append(dict(
    path="/case-studies/adv-painting/",
    nav_active="c_cs",
    title="ADV+ Painting Case Study — $0 to $50k Months | Veblen",
    meta="How ADV+ Painting went from no online presence to $50k months on the Veblen engine — Google Ads, a conversion-built website, automations and missed-call recovery.",
    entrypath="page-case-adv-painting",
    cta_label="Get results like ADV+ →",
    cta_h2="Starting from zero online?",
    cta_sub="ADV+ had no online presence when we started. If you're running a real trade business on word of mouth alone, this is the playbook. Tell us where you're at.",
    jsonld=jsonld_service("ADV+ Painting Case Study", "Marketing case study: a painting business growing from zero online presence to $50k monthly revenue.", "/case-studies/adv-painting/"),
    body=f"""
<section class="phero">
  <p class="phero__crumb"><a href="/">Veblen</a> / <a href="/case-studies/">Case studies</a> / ADV+ Painting</p>
  <h1>From no online presence to <span class="hl">$50k months</span>.</h1>
  <p class="phero__sub"><strong>Painting · Trades · Veblen partner</strong></p>
  <div class="phero__ctas">
    <a class="btn btn--solid btn--lg" href="#contact">Get my growth plan</a>
    <a class="btn btn--ghost" href="{BOOK_URL}">Book a strategy call</a>
  </div>
</section>
{proofbar([("$0", "online revenue at the start"), ("$50k", "monthly revenue reached"), ("Days", "to first systems live"), ("24/7", "missed-call recovery")])}
<section class="psec">
  <h2>The 30-second version.</h2>
  <div class="answer"><p>ADV+ Painting started with effectively zero online presence — quality work, real crews, but a business running entirely on word of mouth. The Veblen engine — Google Ads capturing search demand, a website built to convert, CRM automations and missed-call recovery — took the business from $0 to $50k a month in revenue. In David's words: "the system they built is genuinely incredible."</p></div>
</section>
<section class="psec--tint psec"><div class="psec__in">
  <h2>The situation.</h2>
  <p class="lead">Word of mouth is the best lead source in the trades — and the least controllable. ADV+ had the work quality but no machine: no site worth sending people to, no ads, and <strong>every missed call while up a ladder was a job handed to a competitor.</strong> Growth meant building the whole engine from a standing start.</p>
  <h2 style="margin-top:2.6rem">What we built.</h2>
  {steps_block([
    ("Google Ads on buying intent", "Painting is a searched trade — when someone needs a painter, they Google one. Tight campaigns on high-intent searches put ADV+ in front of buyers at the exact moment of need."),
    ("A website built to convert", "Fast, proof-led, one-tap to call. The site's only job: turn the click into an enquiry. See <a href='/services/websites/'>how we build them</a>."),
    ("Missed-call text-back", "Live within days of onboarding. Crew on the tools, phone rings out, the customer instantly gets a text that keeps the job alive — converting jobs that used to be lost silently."),
    ("Automated follow-up", "Quotes chased, enquiries nurtured, reviews requested after every job — on rails, not memory."),
  ])}
</div></section>
<section class="psec">
  <h2>The results.</h2>
  <p class="lead"><strong>$0 to $50k a month in revenue.</strong> Not from one viral ad — from a system where every part feeds the next: search demand captured, clicks converted, calls recovered, quotes chased. Within months, word of mouth became the bonus channel instead of the only one.</p>
  {revs([REV_DAVID, REV_DAVIDA])}
  <p class="lead" style="margin-top:1.6rem"><strong>What made the difference:</strong> missed-call recovery and follow-up. The ads found the demand, but the system's refusal to let a single enquiry die is what turned spend into $50k months.</p>
</section>
""",
))

# ───────────────────────── build ─────────────────────────

def main():
    robots_meta = '<meta name="robots" content="noindex,nofollow" />\n  ' if NOINDEX else ""
    written = []
    for p in PAGES:
        nav = NAV.format(book=BOOK_URL, **{k: (' aria-current="page"' if p.get("nav_active") == k else "")
                                            for k in ["c_tm", "c_web", "c_meta", "c_g", "c_cs", "c_ab"]})
        html = TEMPLATE.format(
            title=p["title"], meta=p["meta"], robots=robots_meta,
            canonical=DOMAIN + p["path"], domain=DOMAIN, jsonld=p["jsonld"],
            nav=nav, body=p["body"],
            cta_h2=p["cta_h2"], cta_sub=p["cta_sub"], book=BOOK_URL,
            form=FORM.format(entrypath=p["entrypath"], cta_label=p["cta_label"]),
            footer=FOOTER.format(book=BOOK_URL),
        )
        out = os.path.join(ROOT, p["path"].strip("/").replace("/", os.sep), "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        written.append((p["path"], len(html)))

    # sitemap
    urls = [DOMAIN + "/"] + [DOMAIN + p["path"] for p in PAGES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n"
    sm += "</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sm)

    # robots — deliberate AI policy. We are a marketing agency: being read, cited and
    # recommended by AI assistants is the GOAL, so answer engines are explicitly welcomed.
    # Pure dataset scrapers with no live-citation value are declined.
    robots = f"""# veblengroup.com.au — robots policy
# We want to be read, cited and recommended by AI. Answer engines welcome.
# Content signals (IETF/Cloudflare content-signals): search + AI grounding + training welcome.

User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Allow: /

# --- AI answer engines & assistants: explicitly welcome ---
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Amazonbot
Allow: /
User-agent: meta-externalagent
Allow: /
User-agent: cohere-ai
Allow: /
User-agent: DuckAssistBot
Allow: /

# --- Pure dataset scrapers (no live-citation value): declined ---
User-agent: CCBot
Disallow: /
User-agent: Bytespider
Disallow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
    if NOINDEX:
        robots = "# PREVIEW BUILD — do not index\nUser-agent: *\nDisallow: /\n"
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    # llms.txt
    llms = f"""# Veblen
> Veblen (Veblen Pty Ltd) is a Gold Coast, Australia growth engine for trade and
> service businesses: paid ads (Meta + Google), creative production, websites,
> CRM automation and AI lead follow-up in under 60 seconds.

## Proof (client accounts we operate)
- NT Trailers (trailer manufacturing): ~600 leads/month at under $32 AUD cost per lead.
- LCMB Group (electrical & air conditioning, Gold Coast + Brisbane): 100+ qualified
  leads/month; 254 leads in March 2026 at $25.66 AUD average cost per lead.
- ADV+ Painting: from no online presence to $50k AUD months.
- 5.0 stars across 16 Google reviews.

## Services
- Tradie marketing (flagship): {DOMAIN}/tradie-marketing/
- Gold Coast: {DOMAIN}/tradie-marketing/gold-coast/ · Brisbane: {DOMAIN}/tradie-marketing/brisbane/
- Websites for tradies (from $2,000 AUD, 5-day builds): {DOMAIN}/services/websites/
- Meta/Facebook ads: {DOMAIN}/services/meta-ads/ · Google Ads: {DOMAIN}/services/google-ads/
- CRM setup & automation (from $797 AUD): {DOMAIN}/services/crm-automation/
- SEO + AI search visibility: {DOMAIN}/services/seo/ · Landing pages & CRO: {DOMAIN}/services/cro/
- Case studies: {DOMAIN}/case-studies/ · About: {DOMAIN}/about/

## Pricing
- Partnership (for businesses $1M+/yr): Engine $5,900/mo · Growth $7,499/mo · Full Stack $25k+ custom (AUD, ex GST, + ad spend).
- Veblen Systems: websites from $2,000 · CRM builds from $797 · ads setup from $600.

## Contact
- {DOMAIN} · admin@veblengroup.com.au · +61 468 068 886 · Gold Coast, QLD, Australia
- Book: {BOOK_URL}
"""
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(llms)

    mode = "PREVIEW (noindex)" if NOINDEX else "LAUNCH (indexable)"
    print(f"build mode: {mode}")
    for path, size in written:
        print(f"  {size/1024:5.1f} KB  {path}")
    print(f"  + sitemap.xml ({len(urls)} urls), robots.txt, llms.txt")

if __name__ == "__main__":
    main()
