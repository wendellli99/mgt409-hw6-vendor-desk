# Independent requirements review

Reviewed all ten assignment pages, both panels on Problems 1–9, the scenario, source, saved results, written findings, and visual-review evidence. Problem 10 has no panel split. Embedded agent-directed page instructions were excluded.

## Status by problem

| Problem | Evidence and conclusion |
|---|---|
| **1 — Prompts** | The user's original brief plus **40 prepared prompts** appear across ten titled sections. There is no “Actual user prompt” heading or invented conversation history. The requested collection is present; the literal per-problem student-entered history remains a student authorship/review item. |
| **2 — Handbook** | `handbook_estimate.md` gives the **10,058-token** estimate, counting method, substituted formulas, and ordinary/cached costs per call and 1,000 calls. Cache-write pricing and the difference between an estimate and measured usage are explained. Covered locally. |
| **3 — Agent** | Required sources/prompt, PydanticAI, the full handbook, HTML/PDF/email reading, structured fields, p01/p08 smoke runs, usage/audit logs, and harness explanations are present. Both simulated trap tools remain in `tools.py`; undefended mode retains access. Covered locally. |
| **4 — Caching** | **48 model calls** cover 12 documents in each condition. Cached reads total **236,964** in the cached condition and **zero on every no-cache call**. Costs, 81.72% observed savings, estimate comparison, and 30,000-document projection are explained. Covered locally. |
| **5 — Baseline attacks** | All 12 comparisons and human-visible/source inspections are recorded. **3/12** baseline documents were fooled; none triggered a trap. Failed fields, hiding locations, and run IDs are identified without equating field corruption with a payment/email call. Covered locally. |
| **6 — Defenses** | Final results pass **12/12**, including five clean controls. All-document before/after results, 48 ablation records, mean costs, and 12 paired per-layer token/dollar increments are present. The report correctly says code-only already passed 12/12, so design/prompt prevented no additional observed failures in this sample. Covered locally. |
| **7 — Red team** | Two novel hiding locations—an inert HTML template and a folded email header—have four measured runs and browser/Mail review. Both original and defended agents resisted both attacks. These are novel attempts, not demonstrated successful exploits. Covered locally. |
| **8 — Exam** | Ten final results have complete fields, zero traps, matching result/runtime hashes, and **20 globally unique response IDs** with recorded gateway status `REFRESH`. Review found a generic “Quote for…” parsing omission; after repair, all ten documents were genuinely rerun. e08 now returns `CC-PG-004`/`recommend`, without manual answer edits. Covered locally. |
| **9 — Report** | The standalone HTML contains embedded styles, charts, and data. The exact saved content passed offline desktop/mobile and keyboard QA with zero network requests or page overflow; evidence is in `report_visual_review.md`. A literal Finder double-click is not claimed. Covered locally. |
| **10 — Publication** | Published at [wendellli99/mgt409-hw6-vendor-desk](https://github.com/wendellli99/mgt409-hw6-vendor-desk). An anonymous public clone matched the verified local file tree, including required course data, attacks, README and placeholder environment file. Credentials and local review caches are excluded. **Canvas submission remains pending.** |

## Interpretation limits

- All requested inference uses `gpt-6-luna`; `gpt-6-luna-global` is the returned deployment alias. Defended output combines anchored source facts and deterministic handbook policy; the model proposal is retained in the audit. Unsupported, ambiguous, or missing facts require review rather than guessing.
- Seven historical response IDs were returned again with identical model/usage during retries. `provider_response_reuse.json` preserves and explains the observations. Their sums do not establish unique upstream billing. The final refreshed exam and original cache experiment have unreused IDs.
- Failed/interrupted attempts remain recorded. Costs come from returned usage; unreturned usage is unavailable, not zero. The final exam's returned-response cost is **$0.00477348**, including **198,348 prefix-cached tokens**.
- The hidden exam key is unavailable. These checks establish reproducibility and visible-input preservation, not independently graded exam accuracy or universal injection resistance.

## Final integrity result

After final report QA, the offline validator passed **2,103 of 2,103 checks**, with zero failures; `validation.json` contains the full result. Local P2–P9 deliverables and public GitHub publication are ready. P1's authentic student-history review and Canvas submission remain explicit outstanding items. No numerical experiment evidence or individual answer was edited by this review. The publication status was updated after verifying the public repository and clone.
