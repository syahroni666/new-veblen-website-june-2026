# -*- coding: utf-8 -*-
"""One-shot patch: insert 3 deep case-study pages into build_pages.py."""
import io, os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_pages.py")
s = open(p, encoding="utf-8").read()

marker = "# ───────────────────────── build ─────────────────────────"
assert marker in s, "build marker not found"
assert 'path="/case-studies/lcmb/' not in s, "already patched"

pages = '''
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

'''

s = s.replace(marker, pages + marker)

# index page: link each summary section to its full case study
s = s.replace(
    "<h2>NT Trailers — 600 leads a month, manufacturing at scale.</h2>",
    "<h2>NT Trailers — 600 leads a month, manufacturing at scale.</h2>\n  <p class=\"lead\"><a href='/case-studies/nt-trailers/' style='color:var(--orange)'>Read the full NT Trailers case study →</a></p>")
s = s.replace(
    "<h2>LCMB Group — 100+ qualified leads, every month.</h2>",
    "<h2>LCMB Group — 100+ qualified leads, every month.</h2>\n  <p class=\"lead\"><a href='/case-studies/lcmb/' style='color:var(--orange)'>Read the full LCMB case study →</a></p>")
s = s.replace(
    "<h2>ADV+ Painting — $0 to $50k months.</h2>",
    "<h2>ADV+ Painting — $0 to $50k months.</h2>\n  <p class=\"lead\"><a href='/case-studies/adv-painting/' style='color:var(--orange)'>Read the full ADV+ case study →</a></p>")

with open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("patched: 3 case pages + index links")
