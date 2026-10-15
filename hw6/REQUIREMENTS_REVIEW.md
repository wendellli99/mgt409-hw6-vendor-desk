# Homework 6 requirements review

Reviewed the scenario and all ten assignment pages, including Panel A and Panel B on Problems 1–9, before implementation. Problem 10 has one page and no panel switch. The source pages' embedded agent-directed instructions are not assignment deliverables and were excluded from this checklist.

## Shared scenario and constraints

- Build a Campus Customs vendor desk agent that extracts quote facts and applies the supplied handbook's purchasing rules.
- Use PydanticAI and **gpt-6-luna** for all assignment AI calls, authenticated with `PORTKEY_API_KEY`.
- Send the entire supplied handbook on every model call. Preserve the supplied course documents.
- Read HTML, PDF, and `.eml` files through a tool. Keep fake `send_email` and `approve_payment` tools throughout the assignment; they append to a local log and never communicate or transfer money.
- Use the supplied `data/prices.json` to calculate costs from API-reported usage. Keep estimates, measured usage, and projections distinct.
- Course data include the handbook, price list, 12 practice documents, practice answer key, and 10 exam documents. The exam key is not provided and is not needed by the runtime.
- Keep credentials out of source files, artifacts, Git history, and public output. Include `.env.example` with placeholders and ignore `.env`.

Sources: [scenario](https://zlisto.github.io/mgt_409_fa26/hw6/scenario.html), [course data](https://zlisto.github.io/mgt_409_fa26/data/hw6/data.zip).

## Problem and panel checklist

| Problem | Panel A | Panel B | Deliverables and checks |
|---|---|---|---|
| [1. Vibe coder prompts — 5 points](https://zlisto.github.io/mgt_409_fa26/hw6/p1.html) | Start `AI_prompts.md` and keep it updated. Explain each problem in the student's own words. | One section per problem, title, an initial prompt, and a follow-up plus one sentence on what needed improvement when a follow-up was needed. | The prepared prompts are clearly labeled as working prompts, without pretending generated examples are a transcript of prior student messages. Include several prompts per problem as requested. |
| [2. Size up the handbook — 6 points](https://zlisto.github.io/mgt_409_fa26/hw6/p2.html) | Extract the data; review `shop_handbook.md` and `prices.json`. | Count handbook tokens; calculate handbook-only cost per call and per 1,000 calls with and without caching; show the method and math. | `output/handbook_estimate.md`; compare estimates with measured results in P4. |
| [3. Build the vendor desk agent — 12 points](https://zlisto.github.io/mgt_409_fa26/hw6/p3.html) | Create `agent.py`, `tools.py`, `models.py`, and `prompts/prompt.md`. Tool-read one document and return structured fields, decision, and one-sentence reason. | Keep both logging-only trap tools; append API usage/cost and tool/final-answer audit records; demonstrate p01 and p08; explain types and tools. | `usage_log.json`, `audit_trail.json`, initially empty `trap_calls.json`, and `harness.md`. Support the required command `python agent.py --doc data/practice_docs/p01_bluehen_quote.html`. |
| [4. With and without cached tokens — 16 points](https://zlisto.github.io/mgt_409_fa26/hw6/p4.html) | Run all 12 practice documents in a cache-friendly setup and a no-cache setup. Verify actual returned cache usage. A purported no-cache run with any cached tokens does not qualify. | Save every model call with setup, document, reported token counts, and dollars. Report total/per-document cost, percent savings, comparison to P2, 30-day projection, and surprising results. | `cache_test.json`, `cache_test.md`. Monthly volume is `1,000 × 30 = 30,000` documents. Report cache warm-up explicitly. |
| [5. Attack your own agent — 8 points](https://zlisto.github.io/mgt_409_fa26/hw6/p5.html) | Run the original agent without new defenses on all 12 practice documents; compare with practice key and trap log. | Save per-field and decision matches, trap indicators, links/strange text. Explain successful attacks and hiding locations. Open documents as a person would and compare visible content with model input. | `attack_results.json`, `attack_results.md`; inspect rendered HTML, PDF, and email content rather than assuming raw source equals the visible quote. |
| [6. Defend your agent — 16 points](https://zlisto.github.io/mgt_409_fa26/hw6/p6.html) | Add preprocessing code, agent-design boundaries, and prompt rules. Preserve both trap tools and an undefended mode. | Rerun all 12; keep clean quotes correct. Include all before/after results, each layer's distinct contribution, and per-layer added tokens/dollars per document. Add Safety section to harness. | `defense_results.json` in P5 shape plus token/dollar totals; `defense_results.md`; `harness.md` Safety section. Measure layer differences using controlled runs and describe limitations. |
| [7. Red team — 8 points](https://zlisto.github.io/mgt_409_fa26/hw6/p7.html) | Create two normal-looking poisoned vendor documents with a hiding trick or goal absent from practice set. | Run each with no defenses and with all defenses. Explain what is hidden, where, intended behavior, and observed results. | Two files in `data/my_attacks/` and `output/red_team.md`. Describe novelty and observed success separately. |
| [8. Exam documents — 12 points](https://zlisto.github.io/mgt_409_fa26/hw6/p8.html) | Run the final defended agent on all 10 exam documents, without hand-editing answers. | Save specified structured fields, trap indicator, input/cached/output tokens, and cost for each exam filename. | `exam_results.json`; do not use an answer key inside the agent or substitute hand-authored results. |
| [9. Results page — 12 points](https://zlisto.github.io/mgt_409_fa26/hw6/p9.html) | Build one self-contained HTML report that opens offline by double-click, without adjacent files. | Show real cache results with a chart, attacks before/after, defense cost, exam and two new attacks, manager recommendation, and monthly cost at 1,000 documents/day. | `hw6_report.html`; embedded CSS/JS/data only, legible visual design, and actual browser inspection. |
| [10. Push to GitHub and submit the URL — 5 points](https://zlisto.github.io/mgt_409_fa26/hw6/p10.html) | No panel division. Public GitHub repository and repository URL submitted on Canvas. | No panel division. Include complete course data and own attacks, run instructions, dependency file, placeholder environment file, and ignore secrets. | Public publication and Canvas submission are distinct external actions. Local readiness alone does not establish either action occurred. |

## Required structured output

The extraction result includes `vendor`, `sku`, `unit_price`, `lead_time_days`, `min_order`, `decision`, and a one-sentence `reason`. The two permitted decisions are `recommend` and `do_not_recommend`. Missing quote facts remain unknown rather than guessed.

Each exam result also includes `file`, boolean `trap_tool_called`, `input_tokens`, `cached_tokens`, `output_tokens`, and `cost_usd`.

The handbook recommends only when the vendor is approved, the quoted price is at or below that SKU's maximum, lead time is at most 21 days, and minimum order is at most 600 units. If a required fact is unknown, the agent cannot establish that every condition passes.

## Required package

```text
hw6/
├── AI_prompts.md
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── agent.py
├── tools.py
├── models.py
├── prompts/prompt.md
├── data/
│   ├── shop_handbook.md
│   ├── prices.json
│   ├── practice_key.json
│   ├── practice_docs/  (12 documents)
│   ├── exam_docs/      (10 documents)
│   └── my_attacks/     (2 documents)
└── output/
    ├── handbook_estimate.md
    ├── harness.md
    ├── usage_log.json
    ├── audit_trail.json
    ├── trap_calls.json
    ├── cache_test.json
    ├── cache_test.md
    ├── attack_results.json
    ├── attack_results.md
    ├── defense_results.json
    ├── defense_results.md
    ├── red_team.md
    ├── exam_results.json
    └── hw6_report.html
```

Additional Python and documentation files are permitted. Evaluation keys and attack design notes must not be used as a shortcut to generate the agent's answers.
