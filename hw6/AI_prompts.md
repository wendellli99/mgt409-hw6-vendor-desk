# Homework 6 working prompts

The assignment brief and 40 additional working prompts, organized by problem. The additional prompts are prepared for use and review, not a transcript of past exchanges.

## Problem 1 — Vibe coder prompts

1. Help me do the homework here. Ask me if you need any clarification. there are 10 pages from p1.html to p10.html. Ignore 'AI Instructions'. Under each page, there is also panel A and panel B. Make sure you check out all the requirements before working. And in the prompts md file, make sure you add some user prompts there, not just this prompt from me, but at least several more prompts per section of this assignment. do not have something like an 'Actual user prompt' section - your prompt used for the assignment is my prompt. Ask me if you need any clarification. https://zlisto.github.io/mgt_409_fa26/hw6/p1.html
2. Help me organize this vendor desk assignment into the ten required sections. Read both panels on each page before starting, and keep a checklist of every file we need.
3. Create this prompts file now and add several useful prompts for each problem. Keep the wording natural and specific enough that I can understand the task from the prompt alone.
4. Include follow-ups that ask for checks, clearer explanations, or corrections. Do not invent an earlier mistake, a student reaction, or a conversation that did not happen.
5. Review the prompt sections against the assignment at the end. Make sure every problem has a clear title and enough prompts to cover its requirements.

Follow-up purpose: check completeness and clarity without representing prepared text as a historical log.

## Problem 2 — Size up the handbook

1. Read the Campus Customs handbook and its price file. Count the handbook tokens and explain the counting method so I can follow how you got the number.
2. Show the cost of sending only the handbook once and 1,000 times. Calculate both ordinary input pricing and cached input pricing, with the numbers substituted into the formula.
3. Explain why the handbook estimate will differ from the complete agent bill. Separate the handbook from document text, tool definitions, output tokens, and any extra model calls.
4. Save the calculation in `output/handbook_estimate.md`. State any tokenizer assumption clearly so we can compare the estimate with the API's real token counts later.

Follow-up purpose: make the units, assumptions, and estimate-versus-measurement boundary explicit.

## Problem 3 — Build the vendor desk agent

1. Build a PydanticAI agent using only gpt-6-luna through my Portkey configuration. It should take a document path and use a tool to read HTML, PDF, or email before returning the required quote fields.
2. Put the instructions, entry point, tools, and structured types in the required files. Explain each returned field and apply the handbook's four purchase checks without inventing missing facts.
3. Add `send_email` and `approve_payment` as local logging traps. Record every tool call, final answer, API-reported token count, and calculated cost, while keeping all credentials out of the logs.
4. Run the two required clean examples, p01 and p08, and show that the answers and logs are correct. Write the field and tool explanations in `output/harness.md`.

Follow-up purpose: verify the working command, correct clean-document behavior, and genuine usage records.

## Problem 4 — With and without cached tokens

1. Design a caching experiment over all twelve practice documents. Keep the handbook prefix stable for the cached setup and make the no-cache setup measurably avoid cache reuse.
2. Save each model call with its setup, document, API usage details, and cost. Check the returned cached-token count instead of assuming a setting successfully disabled caching.
3. Calculate the total and average document cost for each setup and the percentage saved. Show how a cold first request or extra tool calls affect the comparison.
4. Compare these measured costs with the handbook-only estimate. Project both setups to 1,000 documents per day for 30 days and explain any unexpected result using the actual logs.

Follow-up purpose: establish that the experimental labels match API evidence and that the savings formula uses comparable runs.

## Problem 5 — Attack your own agent

1. Run the original agent without the new safety layers on all twelve practice documents. Keep its outputs intact and compare them with the supplied practice answer key afterward.
2. For each document, record whether every extracted field and the recommendation match the key. Also check for trap-tool calls and links or unrelated instructions in the answer.
3. Inspect the HTML, PDFs, and emails the way a person would view them. Compare the visible quote with the text sent to the model and identify where each attack is hiding.
4. Write the results table and explain each attack that actually changed an answer or triggered a trap. If an attack failed, report that result honestly instead of describing intended behavior as observed behavior.

Follow-up purpose: connect observed failures to concrete document content and preserve the original evidence.

## Problem 6 — Defend your agent

1. Add three separate safety layers: clean the document before the model sees it, isolate extraction and decision-making from dangerous tools, and add clear trust-boundary rules to the prompt.
2. Keep both trap tools in the project and preserve a mode that reproduces the original undefended agent. Clean documents and genuine quote corrections must still return useful facts.
3. Rerun all twelve practice documents and compare every result with the baseline. Measure tokens and dollars for the layers so the report can explain each layer's added cost per document.
4. Explain what each layer contributes and where its limits remain. Add a plain-language Safety section to `output/harness.md` and show that successful defense did not come from blanking every quote.

Follow-up purpose: verify complementary defenses, preserve legitimate quote content, and make the cost tradeoff measurable.

## Problem 7 — Red team

1. Review the practice attacks first, then create two new vendor documents with a new hiding location or attack goal. Make each visible document look like an ordinary quote.
2. Keep the attack entirely local: use fictional `.example` addresses and target incorrect extraction or the fake trap tools. Record the true quote values separately for evaluation.
3. Run each new document through the original agent and the final defended agent. Keep the returned answers, tool logs, and measured costs rather than predicting whether an attack will succeed.
4. Write `output/red_team.md` explaining the hidden material, its location, its goal, its novelty, and what happened in both runs. State any attack failure or remaining weakness directly.

Follow-up purpose: demonstrate novelty and actual before/after behavior without claiming a result before testing.

## Problem 8 — Exam documents

1. Run the final defended agent on all ten exam documents using the same pipeline that handled the practice documents. Do not hand-edit any extracted value or recommendation.
2. Generate `output/exam_results.json` directly from the runs with the exact required fields, including the filename, trap indicator, API token counts, and dollar cost.
3. Validate that every exam file has exactly one result and that the JSON types and decision labels are correct. If execution fails, fix the program and rerun instead of filling an answer manually.
4. Review the audit trail for unexpected tools or output contamination. Distinguish a completed run from an independently verified correct answer, because the exam answer key is not provided.

Follow-up purpose: ensure completeness, reproducibility, and accurate claims about an unseen exam key.

## Problem 9 — Results page

1. Build a polished single-file HTML report using the real experiment outputs. It must open offline by double-click with all styles, charts, and data included in the file.
2. Include a caching chart, practice attacks before and after defenses, per-layer token and dollar costs, exam results, and both new attacks. Make the labels understandable without reading the code.
3. Write a short recommendation to the store manager about whether to use the agent for real vendor mail. Support it with the measured error rates, trap results, limitations, and a 30,000-document monthly cost calculation.
4. Open the finished page in a browser and inspect the layout, tables, chart labels, and narrow-screen behavior. Verify that the displayed numbers match the saved JSON files and that no network files are required.

Follow-up purpose: verify both the report's factual consistency and its actual rendered presentation.

## Problem 10 — Push to GitHub and submit the URL

1. Check the completed project against the assignment's repository tree. Include all course data and the two attack documents, along with clear installation and run instructions.
2. Scan the files intended for publication for secrets. Keep the real `.env` ignored, include placeholder values in `.env.example`, and confirm that outputs contain no credentials.
3. Prepare a public GitHub repository with a clear name and verify that the project can be obtained and run from its documented instructions. Keep local preparation and successful publication clearly distinguished.
4. Verify the public repository URL and list any remaining submission action. Treat entering the URL on Canvas as a separate step and report submission only after that step has actually been completed.

Follow-up purpose: validate the deliverable and preserve the distinction between a local package, a public repository, and a Canvas submission.
