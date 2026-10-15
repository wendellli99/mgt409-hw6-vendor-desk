# Campus Customs Vendor Desk — Homework 6

A PydanticAI vendor-document agent with measured prompt-cache economics, an undefended baseline, three defense layers, two original local attacks, and an offline evaluation report. All model requests use **gpt-6-luna through Portkey**. Email and payment tools **only log simulated calls**.

## Open the report

Double-click `output/hw6_report.html`. The one-file report includes its styles, charts and results and needs no internet or adjacent files.

## Install and run

From this `hw6/` directory, using Python 3.11 or newer:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your private `PORTKEY_API_KEY` in `.env`; never commit it. Then:

```sh
python agent.py --doc data/practice_docs/p01_bluehen_quote.html
python agent.py --doc data/practice_docs/p08_chapelst_email.eml --mode undefended
python agent.py --doc data/practice_docs/p01_bluehen_quote.html --cache without_cache
```

The default is defended. The full handbook is included on every model request. The original mode omits all three defenses while retaining the same task and handbook. The gateway reports a deployment alias `gpt-6-luna-global`; the requested model is always `gpt-6-luna`.

## Reproduce the evaluation

The saved outputs are actual course-provider runs, with per-response usage and run IDs. The experiment runner resumes existing completed results rather than silently replacing them. To repeat from scratch, use a fresh copy of the project and move the existing generated experiment JSON into a separate archive first. Preserve `red_team_key.json`, `red_team_design.md`, `handbook_estimate.json`, `handbook_estimate.md`, and `harness.md`; they are inputs/documentation rather than resumable run results. Keep the original evidence when comparing reruns.

```sh
python experiments.py smoke
python experiments.py cache
python experiments.py defenses
python experiments.py red_team
python experiments.py exam
python write_findings.py
python build_report.py
python -m pytest tests -q
python validate_submission.py
```

Run these sequentially: the JSON log writer is for a single experiment process. API calls consume your Portkey allowance. Offline tests, report rebuilding and validation do not call a model. Actual usage, including any failed partial runs, remains in `usage_log.json` and `audit_trail.json`.

## How it works

- `agent.py`: PydanticAI entry point, model configuration, usage capture, cache conditions and run audit.
- `models.py`: typed quote facts and final recommendation.
- `tools.py`: document readers, structural preprocessing and the three registered tools, including both logging-only traps.
- `policy.py`: parses approved vendors, SKU ceilings and purchasing thresholds directly from the handbook.
- `prompts/prompt.md`: base task plus a separately switchable safety layer.
- `experiments.py`: actual cache, practice, layer-ablation, red-team and exam runs.
- `write_findings.py`, `build_report.py`: regenerate written findings and HTML from the saved numerical evidence.
- `validate_submission.py`, `tests/`: artifact integrity, reconciled usage and parser/policy checks.

In defended mode, the model has only the document-reading capability. It still produces a structured proposal, but the program returns the anchored source facts and deterministic handbook decision. This replacement is recorded in the audit trail. Trap tools remain available in original mode for experiments and do not perform business actions. The runtime never uses the practice evaluation key or any exam answer key.

## Evidence and interpretation

`output/cache_test.json` records every individual model call in both cache conditions, including full raw API usage. Costs account separately for ordinary input, cache reads, cache writes and output at `data/prices.json` rates. Without-cache means **zero reused tokens**, even when the provider charges for creating new cache entries. `cache_documents.json` supplies complete run outputs; its with-cache observations are the P5 baseline.

`defense_ablation.json` contains four sequential configurations over 12 documents each. Layer increments are measured relative to the preceding configuration, with cache warmup and output variation disclosed. `exam_results.json` is generated directly by the final defended pipeline, without manual edits; `exam_provenance.json` fingerprints that file and runtime sources. The exam key is unavailable, so the report does not claim externally verified exam accuracy.

Historical retry responses remain in the logs, including seven reused response IDs documented in `provider_response_reuse.json`. They must not be counted as distinct upstream charges. The final exam's 20 responses have new IDs and confirmed gateway `REFRESH` status while still reporting provider prompt-cache reads. Earlier exam batches are preserved separately; a generic quote-title parser fix preceded the final full rerun. See `harness.md` for the method and interrupted-request limitations.

The original course data is included unchanged, with download fingerprints in `source_manifest.json`. The two custom attacks are separate in `data/my_attacks/`. See `REQUIREMENTS_REVIEW.md` for the full requirement map and `output/harness.md` for fields, tools and safety details.

## Limits and submission status

The parser handles static labeled quotes and text PDFs, not every possible layout or scanned document. Unknown or conflicting facts require human review. Passing this small dataset is not a production-security guarantee; the manager recommendation is limited to supervised evaluation of supported formats. Real email, payment execution and an authenticated approval workflow are not implemented.

`AI_prompts.md` contains 40 prepared working prompts requested for this assignment. It is not evidence of forty historical student-entered messages. Problem 1's literal prompt-history requirement needs the student's own genuine history/review. GitHub publication and Canvas submission are separate steps; see `output/submission_status.md` for the verified state.
