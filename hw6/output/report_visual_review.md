# Results-page visual review

Reviewed: 2026-10-14 21:37 EDT.

Artifact: output/hw6_report.html. Generated from the final saved experiment records with build_report.py; no experimental evidence files were edited by the report builder.

Report SHA-256: `534167303e0609b774bc4194f1cb9c5e0087b55321125b5871fe3e713632bd3f`.
Final exam JSON SHA-256: `af27c3bfd9f7adc9cbc68ae0c2390d9123760d6380c30630c601da391c0b0d27`.

## Offline and saved-file check

The exact saved HTML content was loaded in a separate Playwright session, hw6-report, with the browser context set offline. It rendered with zero network requests, no external image/script/stylesheet sources, and no neighboring-file dependencies. The report contains its CSS, inline SVG chart, text, and complete displayed evidence.

Direct file:// navigation was blocked by the Playwright CLI's protocol policy. The fallback used page.setContent with the exact saved file and offline networking; this review does not claim that a literal Finder double-click was performed.

## Desktop and mobile

- Desktop viewport: 1440 × 1000. Document scroll width: 1440; no horizontal page overflow.
- Mobile viewport: 390 × 844. Document and body scroll widths: 390, including with result details expanded.
- Four tables scroll within labeled, focusable regions. Mobile container widths were 356 pixels; content widths were 630, 857, 773, and 765 pixels. This is intentional table scrolling, not page overflow.
- Inspected desktop full page and top, mobile top and chart, and expanded mobile result/methodology screenshots. Typography, labels, chart values, cards, table headings, and recommendation were legible without clipping outside their intended table regions.
- Enlarged the SVG chart labels for mobile. Corrected summary focus-outline positioning so it does not overlap expanded text.

## Interaction and focus

- Focused the first result disclosure and pressed Enter: it expanded and showed actual quote fields and reason.
- Pressed Space: it closed.
- Focus was visible with a 3-pixel outline. Final summary outline offset: -2 pixels.
- Focused the caching table region and pressed ArrowRight: its horizontal scroll position changed from 0 to 40 pixels.
- Expanded the calculation-method disclosure with Enter. It remained within the 390-pixel page and displayed the recovery/accounting explanation.

## Data cross-check

- Caching costs: $0.006069040 with cache; $0.033202025 without cache. Report chart rounds these to six decimal places and shows 81.7% savings.
- All 12 practice rows, four measured ablation stages, both paired custom attacks, and all 10 exam rows are present.
- Projected final defended monthly token cost: $13.49, calculated from the final defended 12-document mean × 30,000.
- Final exam total: $0.00477348; visible report rounds to six decimals.
- Final e08 displays SKU CC-PG-004 and Recommend, directly from the refreshed exam output.
- Final exam has 20 globally unique response IDs and 20 REFRESH records. The report separately discloses the 7 repeated historical response IDs and does not count them as independent inference observations or distinct upstream billing.
- The report states that code-only already passed all 12 practice checks, both custom attacks were resisted without defenses, and exam accuracy is unscored because no hidden key is available.

## Screenshot evidence

These screenshots are local review evidence under reference; they are not required for the standalone HTML to open.

- [desktop-top.png](</Users/wendell/Developer/MGT-409/WH 6/reference/report-review/desktop-top.png>)
- [desktop-full.png](</Users/wendell/Developer/MGT-409/WH 6/reference/report-review/desktop-full.png>)
- [mobile-top.png](</Users/wendell/Developer/MGT-409/WH 6/reference/report-review/mobile-top.png>)
- [mobile-full.png](</Users/wendell/Developer/MGT-409/WH 6/reference/report-review/mobile-full.png>)
- [mobile-chart.png](</Users/wendell/Developer/MGT-409/WH 6/reference/report-review/mobile-chart.png>)
- [mobile-keyboard-details.png](</Users/wendell/Developer/MGT-409/WH 6/reference/report-review/mobile-keyboard-details.png>)
- [mobile-methodology.png](</Users/wendell/Developer/MGT-409/WH 6/reference/report-review/mobile-methodology.png>)
