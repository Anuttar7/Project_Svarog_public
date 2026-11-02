"""Score say-aloud drafts against the task's fixed rubric. Deterministic, no model judges."""
import re, sys, pathlib, json
FACTS = {  # fact -> any of these must appear
 "bag_1bar": ["1 bar", "one bar"], "cte_0.75": ["0.75", "three quarters"], "autoclave": ["autoclave"],
 "5_10x": ["5 to 10", "five to ten"], "not_glued": ["unglued", "not glued", "don't glue", "isn't glued", "slides"],
 "screws_slots": ["slot"], "H14": ["H14"], "O_wrinkle": ["wrinkle"], "caltech": ["Caltech"],
 "seals_grain": ["end grain"], "cost_0.5": ["smaller"],
}
BAD = [r"—", r"\bnot\b[^.]{0,40}\bbut\b", r"key takeaway", r"here's|here is the", r"\bdelve", r"no fluff"]
rows = []
for f in sys.argv[1:]:
    t = pathlib.Path(f).read_text().strip()
    words = len(t.split())
    facts = [k for k, alts in FACTS.items() if any(a.lower() in t.lower() for a in alts)]
    bad = [b for b in BAD if re.search(b, t, re.I)]
    sents = [s for s in re.split(r"(?<=[.!?])\s+", t) if s]
    longest = max(len(s.split()) for s in sents)
    units = len(re.findall(r"\d+(\.\d+)?\s*(mm|bar)", t))
    score = len(facts) - 2 * len(bad) - (2 if not 90 <= words <= 130 else 0) - (1 if longest > 35 else 0)  # why fixed: the rubric written into the task prompt (90 to 130 words, sentences up to 35 words), kept as run
    rows.append(dict(model=pathlib.Path(f).stem.replace("write_", ""), words=words, facts=f"{len(facts)}/{len(FACTS)}",
                     missing=[k for k in FACTS if k not in facts], banned=len(bad), longest_sentence=longest,
                     digit_units=units, score=score))
for r in sorted(rows, key=lambda r: -r["score"]):
    print(json.dumps(r))
