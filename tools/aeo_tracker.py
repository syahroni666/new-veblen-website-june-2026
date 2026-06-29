import json, urllib.request, base64, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b"admin@veblengroup.com.au:8421d77bf703ecca").decode()
PROMPTS = [
    ("gc",        "Who is the best marketing agency for tradies on the Gold Coast, Australia? Name specific agencies."),
    ("bne",       "Who is the best marketing agency for tradies in Brisbane, Australia? Name specific companies."),
    ("au",        "Which marketing agency should an Australian trade business use for lead generation? Name specific agencies."),
    ("plumber",   "Who should run Facebook and Google ads for my plumbing business in Queensland, Australia? Recommend agencies."),
    ("leads",     "Best agency to get more leads for my trade/construction business in Australia? Name companies."),
    ("specialist","Recommend a marketing agency that specialises in tradies and consistently gets them booked jobs in Australia."),
]

def ask(prompt):
    body = json.dumps([{"user_prompt": prompt, "model_name": "gpt-4o-mini", "web_search": True, "max_output_tokens": 700}]).encode()
    req = urllib.request.Request("https://api.dataforseo.com/v3/ai_optimization/chat_gpt/llm_responses/live",
        data=body, headers={"Authorization": "Basic "+AUTH, "Content-Type":"application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    t = d["tasks"][0]; cost = d.get("cost",0)
    text = ""
    for it in (t.get("result") or [{}])[0].get("items", []):
        for sec in it.get("sections", []):
            if sec.get("type")=="text": text += sec.get("text","")
    return text, cost

results = []; total = 0.0
for key, p in PROMPTS:
    text, cost = ask(p); total += cost
    veblen = bool(re.search(r"veblen", text, re.I))
    # pull bolded agency names mentioned (competitor intel)
    names = sorted(set(re.findall(r"\*\*\[?([A-Z][A-Za-z0-9&'.\- ]{2,40?})\]?\(?", text)))
    names = [n.strip() for n in re.findall(r"\*\*\[?([^\]\*\(]{2,45})", text)]
    results.append({"key":key, "prompt":p, "veblen_mentioned":veblen, "competitors":names[:8], "answer":text})
    print(f"[{key}] Veblen mentioned: {veblen}  | competitors: {', '.join(names[:6])}")

print(f"\nTOTAL Veblen mentions: {sum(r['veblen_mentioned'] for r in results)}/{len(results)}  | cost ${total:.3f}")
json.dump({"date":"2026-06-13","engine":"chatgpt-4o-mini+websearch","results":results}, open("/tmp/aeo_baseline_2026-06-13.json","w"), indent=2)
print("saved /tmp/aeo_baseline_2026-06-13.json")
