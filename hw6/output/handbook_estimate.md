# Problem 2: Size up the handbook

The UTF-8 handbook has **10,058 tokens** using tiktoken's `o200k_base` encoding on the text read by Python (newlines normalized consistently with the agent). This is a local estimate of the handbook text only; API message formatting, tool schemas, vendor content and generated answers add tokens. The actual API usage is the measurement in Problem 4.

Use the supplied `data/prices.json`, not a different live pricing page. All rates below are dollars per one million tokens.

| Handbook input condition | Calculation for one call | One call | 1,000 calls |
|---|---|---:|---:|
| Ordinary uncached input | 10,058 × $0.10 / 1,000,000 | $0.00100580 | $1.00580 |
| Already cached input | 10,058 × $0.01 / 1,000,000 | $0.00010058 | $0.10058 |
| Cache creation input | 10,058 × $0.125 / 1,000,000 | $0.00125725 | $1.25725 |

Cached handbook reads cost 90% less than ordinary input. A cache write costs 25% more than ordinary input; caching pays off through subsequent reads. One cold write plus 999 full handbook reads would cost $0.10173667, before any document, tool, or output tokens. These are handbook-per-model-call estimates, not per-document costs: the agent normally calls the model once to request its read tool and again to answer.

Reproduce: `python -c "import tiktoken; from pathlib import Path; print(len(tiktoken.get_encoding('o200k_base').encode(Path('data/shop_handbook.md').read_text())))"`.
