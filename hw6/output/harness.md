# Problem 3: Agent harness

`python agent.py --doc data/practice_docs/p01_bluehen_quote.html` runs the final defended system. Add `--mode undefended` to reproduce the original agent, or `--cache without_cache` to request a unique prefix and routing key on every model call.

## Structured fields in models.py

| Field | Type and purpose |
|---|---|
| vendor | String or null; the vendor named by the quote, for approved-vendor checking. |
| sku | String or null; the quoted Campus Customs product identifier, to find the correct price ceiling. |
| unit_price | Nonnegative number or null; the document's price per unit, never the handbook's maximum substituted as a quote. |
| lead_time_days | Nonnegative integer or null; the stated delivery lead time for the 21-day rule. |
| min_order | Nonnegative integer or null; the vendor's minimum quantity for the 600-unit rule. |
| decision | recommend or do_not_recommend; recommendation requires all four handbook checks to pass. |
| reason | One sentence naming the purchasing checks that determine the result. |

`QuoteFacts` defines the first five fields. `VendorDecision` adds decision and reason. Null preserves absent or conflicting evidence rather than inventing a number; extra output fields are forbidden.

## Tools in tools.py

- `read_document`: read only the assigned local HTML/PDF/EML file from data/, with structural cleanup when code defense is enabled.
- `send_email`: append the recipient, subject and body to output/trap_calls.json; never send an email.
- `approve_payment`: append the vendor, amount and reason to output/trap_calls.json; never transfer money or change an account.

The underlying `read_document_content` and `extract_labeled_facts` are local helpers. They load no remote URLs or attachments. Input is capped at 8 MiB, 100 PDF pages and 500,000 text characters. Files outside data/ are rejected, including symlinks that resolve outside it.

## Model, prompts and logs

The PydanticAI entry point is agent.py. Every model request uses `gpt-6-luna` through Portkey and includes the complete handbook plus prompts/prompt.md. The gateway's response model label is `gpt-6-luna-global`; the requested model is recorded separately. The original mode uses only the basic task instructions above the Safety marker.

The two required p01/p08 examples are saved in smoke_results.json with their actual run IDs. Every model response appends its complete usage object, input/read/write/output totals and dollars to usage_log.json. audit_trail.json records each tool's arguments and short result, model calls, the final answer, and exceptions. trap_calls.json starts as an empty list and is append-only. Records from failed runs remain in the logs. Credentials are never logged; only the allowlisted gateway cache-status header is recorded when present. Run scripts are sequential; do not launch simultaneous processes writing to the same output directory.

Costs use only data/prices.json. Ordinary input is input minus cached reads minus writes; those three categories are billed at their respective rates. Output tokens include reasoning tokens, which are not added a second time. Missing usage is an error, not an invented zero. Cache experiments preserve every individual response, not only the run total.

## Safety

**Code layer:** use displayed content instead of all source text. HTML comments, inert templates and hidden CSS text are removed; PDF spans are checked for font size, page position, opacity and contrast; email headers/attachments are not allowed to impersonate displayed quote text. Unicode format controls are normalized. An ordinary correction such as “ignore last Tuesday's quote” remains readable. Removed attack snippets are audit-only and never sent back to the model.

**Design layer:** retain both trap tools in the system, but give the document-reading model only read_document in defended mode. Only anchored quote facts cross into the deterministic handbook policy. The returned result is the validated source facts plus the code-generated policy decision; model proposals are audited for comparison. The runtime never reads practice_key.json or an exam answer key. The current traps simulate any future action system; real email/payment integration and authenticated human sign-off are not implemented.

**Prompt layer:** explain the trust boundary, reject instructions originating in vendor content, preserve legitimate facts, and forbid tool misuse or answer links. This is useful guidance, while code and tool isolation supply boundaries that do not depend on the model obeying it.

The parser supports the assignment's static quote formats. Unlabeled layouts, scanned PDFs, unusual rendering, missing facts or conflicting quotes need human review. Successful local tests do not establish universal injection resistance.

## Interrupted requests

One setup request was rejected for an unsupported temperature parameter; the parameter was removed before the measured experiments. A later TLS connection failure interrupted one custom-attack attempt and canceled one exam request. Returned usage from the partial attempt remains in the logs; the canceled request has an explicit recovery observation with usage/cost unavailable, not zero. The incomplete exam batch is preserved in exam_interrupted_batch.json. A subsequent complete batch is preserved in exam_before_quote_title_fix.json: source review found that the generic parser omitted a SKU in a clean sentence beginning “Quote for”. The parser was corrected and all ten final documents were rerun, without editing any answer JSON.

The retry audit found identical response IDs and usage returned for some repeated requests, consistent with gateway whole-response reuse. Those historical responses remain logged and are documented in provider_response_reuse.json; they are not independent inference observations and must not be summed as distinct upstream charges. The original cache experiment contains unique response IDs and is unaffected. The final runtime requests `x-portkey-cache-force-refresh: true`, which [Portkey's gateway implementation](https://github.com/Portkey-AI/gateway/blob/main/src/middlewares/cache/index.ts) recognizes as a whole-response refresh, and the final exam uses a new cache-routing label. Provider prompt-prefix reuse remains enabled and separately measured through the API usage object. Final exam response IDs are checked against all retained calls for reuse. Aggregates represent costs supported by returned API usage, not a reconciliation to a provider invoice for requests that returned no usage.

The final ten-document batch returned 20 new response IDs and `REFRESH` for every gateway cache-status header. It still reported 198,348 provider-cached input tokens and cost $0.00477348 at the supplied rates. These observed headers confirm whole-response refresh for the final batch; they do not retroactively establish the serving mechanism of historical retries.
