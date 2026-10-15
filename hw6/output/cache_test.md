# Problem 4: With and without cached tokens

Both conditions run the original undefended PydanticAI agent over all 12 practice documents. Each result normally takes two model calls (read tool, then answer); every call, including any additional tool round, is in `cache_test.json` with its full API usage object. Both use the exact requested model `gpt-6-luna`; the gateway identifies the served deployment as `gpt-6-luna-global`.

## Experimental setup

With cache: a stable prompt, tool schema, full handbook prefix and `prompt_cache_key` across documents. The initial cache write is included. Without cache: a new random nonce is prepended to the first system message and a new routing key is set **on every model request**, including continuations after tools. The handbook is still sent in full. This prevents reused input; it does not promise that the provider will avoid writing a new cache entry. The nonce adds a small measured input overhead to that condition.

Proof from the API: with-cache reports **236,964 cached tokens**; every without-cache call reports **0**, totaling **0**. No cached values were relabeled as uncached. See [OpenAI's caching documentation](https://developers.openai.com/api/docs/guides/prompt-caching) for prefix matching and routing keys; dollar rates here come solely from the supplied course price file.

| Setup | Model calls | Input | Cache reads | Cache writes | Output | Total USD | USD/document | USD/30,000 documents |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| with_cache | 24 | 254,260 | 236,964 | 14,272 | 3,226 | $0.00606904 | $0.00050575 | $15.17 |
| without_cache | 24 | 254,829 | 0 | 251,805 | 2,848 | $0.03320203 | $0.00276684 | $83.01 |

Savings = (without − with) / without × 100 = ($0.03320203 − $0.00606904) / $0.03320203 × 100 = **81.72%**.

## Cost calculation and estimate comparison

For each response, ordinary input = input_tokens − cached_tokens − cache_write_tokens. Dollars = (ordinary × 0.10 + cache reads × 0.01 + cache writes × 0.125 + output × 0.50) / 1,000,000. Output includes reported reasoning tokens: they are already part of output_tokens and are not billed twice. The raw usage records retain the reasoning-token detail.

Problem 2 counted 10,058 handbook tokens: $0.00100580 for ordinary input or $0.00010058 for a fully cached read **per model call**, before all other content. Actual first-call input is 10,442, because it also includes instructions, the user request and tool/output schemas. Tool continuations send the handbook again and add document text and earlier messages. Per-document totals therefore cannot be compared to a single handbook-only call as if they had the same scope.

The surprising charge is cache creation: $0.125 per million is 25% more than ordinary $0.10 input. The without-cache condition has no reads but 251,805 writes, so repeatedly changing the prefix incurs that surcharge. Cached reads cost $0.01 per million, 90% below ordinary input, but total savings are smaller than that headline because outputs, writes and noncached suffixes still cost money. The two conditions can also generate different answer lengths and tool behavior; this is an end-to-end observed comparison, not a controlled equal-output-token simulation.

For 1,000 documents/day × 30 days = 30,000 documents, monthly API cost is measured total / 12 × 30,000: **$15.17 with cache** and **$83.01 without reuse**. This extrapolates this small workload, including one cold start per 12 documents. It excludes hosting, monitoring, human review, taxes and real email/payment operations; production cache expiry and document lengths may differ.
