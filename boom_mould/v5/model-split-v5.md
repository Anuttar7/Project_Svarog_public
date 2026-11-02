# Svarog mould v5: which model did which part, and why

2 Nov 2026. The ask was to split the work by measured strength across models, or show the comparison if one model won every part.

## Who could be tried

Measured 15:30 on 2 Nov:

| Lane | State |
|---|---|
| Claude Opus 5.5 | available |
| Claude Sonnet 5.5, Haiku 5.5 | available (subagents) |
| qwen2.5:7b-instruct, llama3.2:3b | available (local, Ollama) |
| Gemini | quota exhausted until 3 Nov 08:00 |
| Codex / GPT | quota exhausted until 4 Nov 10:07 |
| Copilot | limited until 1 Dec |

So the comparison covers Claude models and two local models only. Gemini and GPT were not tested on any part.

## Per part

| Part | Done by | Tried against | Result |
|---|---|---|---|
| Geometry and calcs (calc5.py) | Opus 5.5 | none | no second lane could run Python-checked engineering calcs; not compared |
| Drawing and layout (drawing5.py, A3 sheet) | Opus 5.5 | none | not compared |
| Adversarial engineering review | Sonnet 5.5 (fresh context) | qwen2.5 7B, llama3.2 3B, same prompt | Sonnet 8 findings, 7 accepted or partly accepted in v5; qwen 0 of 4 valid; llama 0 of 7 valid (review-v5-adversarial.md) |
| Writing (the say-aloud paragraph) | Opus 5.5 | Sonnet 5.5, Haiku 5.5, qwen2.5 7B | rubric score: Opus 10, Sonnet 8, qwen2.5 8, Haiku 6 (bake-v5/) |
| Readability review of the pack, session sheet and drawing | Sonnet 5.5 (fresh context, images only plus HTML) | none | see readability-review-v5.md |

Sonnet reviewed work Opus did, so no model checked its own output.

## The writing rubric

`bake-v5/score_writing.py` is deterministic: one point per required fact present (11), minus 2 per banned pattern (em dash, "not X but Y", signposting), minus 2 outside 90 to 130 words, minus 1 for a sentence over 35 words. Re-run on 2 Nov 15:58 it gives the same scores as above.

Caveats, both real:
- Opus wrote the rubric and the prompt, so the scoring may favour how Opus writes.
- The bake-off prompt used an earlier fact set. Two of its facts were later dropped from v5: the "aluminium face matches Caltech, so 0.835 holds" claim (unsupported, review finding 4) and the "5 to 10 times the pressure needed" margin (review finding 2). The test measures how well each model writes from a fixed set of facts; the pack text was rewritten from the corrected facts.

## Conclusion

Opus won calcs, drawing and writing by default or by score. Sonnet was the only lane whose engineering review held up, and it also did the readability review. The local models added nothing usable on review and came joint second on writing. A fair test of GPT and Gemini waits on their quotas.
