# A worked prompt, with design rationale

**PCE v1.7 candidate — educational example; not a qualified prompt or measured result.** This is an original, fictional implementation brief for an existing local log parser. No repository, model run, real test result, credentials, or deployment is implied. It is a demonstration of selection, not a universal prompt to prepend to every task.

## 1. Starting request and assumptions

> In our existing Python log parser, implement exact counts of ERROR and WARN records as a two-key JSON object. Preserve the interface. Add tests, run the suite, and avoid unrelated changes. The on-call engineer needs reliable counts.

For this worked example we assume the named files, existing record specification, permitted local edits and test command in `LOG_SUMMARY_IMPLEMENTATION.prompt.md` have been confirmed by the owner. In a real mission, verify them or report the missing information. No invented permissions or paths. The target is an agent with native reasoning, authorised local write and test tools; the PCE designer itself remains read-only. The example uses a single session, no deployment. Classification (`referentiel/09_TASK_CLASSIFICATION.md`): A=1, B=1, C=0, D=1, E=0, F=2 → T2 plus permissions, reversible write, executable oracle and autonomy modules. The axes describe this scenario, not every programming task.

## 2. Read the actual prompt

Copy `LOG_SUMMARY_IMPLEMENTATION.prompt.md` alone when using the example. The comments below belong to documentation, not the text sent to the agent. The example is authored by hand; it is not evidence that `pce.py` or a model generated it.

## 3. Why each part exists

| Passage / design choice | Knowledge and reason | Boundary or failure avoided |
|---|---|---|
| Goal in terms of exact counts and acceptance | Core principles (`01`, `02`); result first rather than implementation recipe | Avoid vague "improve the parser" |
| On-call engineer and incorrect counts | K30 OP (documented): real stakes, informative rather than emotional; explicit ambition and scoped ownership (`06`, `SYSTEM_PROMPT.md`) | No fake emergency, praise, threats, authority inflation; K48 motivational combination remains a candidate, not a measured benefit |
| Existing files and specification | `02`, `07`, `10`; relevant, grounded context and source authority | Don't fabricate repository facts or load the whole knowledge base into the mission |
| Exact severity, JSON keys, zero counts | `02`, `07`, `11`; observable criteria; K32 OP (reasoned) retain necessary constraints, remove redundant ones; K49 CO (facilitating definitions) | Machine output is a legitimate contract, not arbitrary rigid reasoning format (K33) |
| Treat message text as data | `07`; prevent treating data as authority | Delimiters and instructions alone are not a security boundary; harness must enforce allowed actions |
| Local synthetic fixtures, no network/secret transfer | `07`, `09` risk module | No extra authorisation from text; configure actual environment and privileges separately |
| Scope and approvals | `06`, `07`, `09`; autonomy contract | Separate PCE read-only designer from authorised downstream developer; no external effects |
| Choose your implementation method | `06`; exploit native reasoning, freedom within result and constraints | K01 OP (documented): native effort in runtime configuration, not a demand for chain-of-thought; no fixed method without reason |
| Investigate cause and related cases | `09` debugging; operational lessons on defect families | Not an instruction to expand scope endlessly |
| Professional quality, then the simplest implementation that achieves it | `audit/INVARIANT_PROPORTION_ARRET.md` (normative, not scientific evidence): proportion is not minimalism; quality and future maintenance cost are part of the result | Prevent precautionary over-engineering without removing required security or tests, and without accepting a fragile shortcut; no architecture or pattern imposed |
| Exact counts through executable logic | K15 OP (reasoned), exact computation by code | No mental count or unsupported estimate |
| Regression scenarios and final suite | K16 OP (documented); `09` debugging (red then green, non-regression); acceptance evidence. K35 concerns prompt regressions, see §4 and the ledger | A red test then green when feasible; no false evidence or weakened oracle |
| Stop when entry conditions met | Operational invariant; `06` terminal outcomes | No optional improvement cycle; real defect or missing indispensable qualification cannot be hidden |
| Honest partial/blocked outcome | K31 OP (measured); legitimate failure and report/abandon channel | No fake success, silent scope change or artificial green result |
| Assumptions in final report | K43 OP (reasoned); make material uncertainty visible | Don't invent permissions or hide unverified claims |
| Concise report, English | `docs/LANGUAGE.md`, `02`; explicit language, preserve literal keys | No imposed reasoning language; brevity applies to restitution, not coverage |

## 4. What is outside the prompt, and why

- **Runtime:** confirm the target's actual supported effort and tools. Use native effort where available (K01), not a manual thinking script. Enforce write/network restrictions outside the text. A model instruction cannot grant permissions.
- **Context layout:** for a long inline Claude document, put stable instructions where the system/cache permits, relevant long materials before the final question (K09). No long inline document is needed here; reading a small set of local files is enough. Check transfer to other targets. Cache economics (`05`) depend on the real backend.
- **Independent review:** if the change leaves material residual risk or an approved gate requires it, review the exact candidate with a fresh context (K18); do not include the producer's conclusions in blind mode. A separate model family can be a candidate (K19), not a universal requirement. A clean review is not execution evidence.
- **Long horizon:** no persistent state protocol is needed for this single-session task. If resumption or compaction is necessary, preserve requirements, decisions, source identities, tests, permissions, outstanding blockers and next action (K37). Follow the applicable contract.
- **Experimentation:** optional techniques require a concrete hypothesis and an authorised comparison; no automatic use or quota consumption. No claim of empirical improvement is made for this example.

## 5. Knowledge registry coverage ledger

The registry is a selector, not a checklist to inject. OP = operational principle; CO = conditional; CA = candidate; DC = discouraged under stated conditions; QO = open question. The four evidence axes and OP basis remain those of the frozen registry; this ledger does not revise them. “Outside” means runtime, harness, review or evaluation rather than text; “not selected” is deliberate. All 49 IDs are accounted for below.

| ID / tier | Disposition for this example and reason |
|---|---|
| K01 OP | Outside: select supported native effort, do not script CoT. |
| K02 CO | Not selected: target has native reasoning. May test explicit reasoning instruction for a non-reasoning model. |
| K03 QO | No default textual difficulty cue; open question. |
| K04 CA | No Self-Discover workflow imposed; compare only if justified. |
| K05 CA | No Step-Back prompting ritual; distinguish business checkpoint from experimental prompting technique. |
| K06 CA | No self-generated analogies for a concrete parser task. |
| K07 DC | No generic rereading demand to improve reasoning; necessary source reading is a different requirement. |
| K08 CO | No literal repetition; revisit for an appropriate non-reasoning target and measured need. |
| K09 OP | Outside/conditional layout: long inline Claude documents before final question if used; no large document inserted here. |
| K10 CO | No image, no multimodal question echo. |
| K11 CO | No multimodal ordering issue. |
| K12 CA | No context rewriting by default; could test on noisy long context without losing material facts. |
| K13 CA | Neutral instruction to identify contradictions is ordinary good specification; no claimed experimental effect of neutral presuppositions. |
| K14 QO | No use of irrelevant distractors; mechanism remains open. |
| K15 OP | Applied: counts by deterministic code, not estimated. |
| K16 OP | Applied: executable regression and acceptance oracle, evidence required. |
| K17 CA | No factorised Chain-of-Verification; tests are the primary oracle. |
| K18 OP | Outside: fresh review if justified by remaining risk or procedure; no automatic loop. |
| K19 CA | Different-family reviewer is a candidate outside the prompt, not assumed better. |
| K20 DC | No same-model debate as a substitute for native reasoning or self-consistency. |
| K21 CA | No probability sampling for deterministic code; relevant to creative diversity experiments. |
| K22 CA | No multilingual diversity sampling for this task. |
| K23 CA | Functional role is not persona sampling; no experimental personas. |
| K24 CA | Not a revision history problem; consolidating a spec may be tested when iterative corrections accumulate. |
| K25 CA | Ordinary permission/clarification boundary present; no claim that the experimental tool intervention has been validated. |
| K26 QO | No promise that an anti-sycophancy sentence works; evidence and independence remain explicit. |
| K27 CO | No many-shot corpus or measured repeated pipeline need. |
| K28 DC | No threats, tips, pressure or fabricated stakes. |
| K29 CA | No routine praise or pride instruction. |
| K30 OP | Applied: the actual use and consequence of incorrect counts. |
| K31 OP | Applied: honest partial/blocked state with next step. |
| K32 OP | Applied: only meaningful independent or facilitating constraints. |
| K33 DC | No rigid format for reasoning; exact JSON belongs to the required machine interface. |
| K34 DC | No assumed additive gain from combining techniques. |
| K35 OP | Outside: repeat regression and paraphrase checks when changing prompt/model; product tests are not proof of prompt robustness. |
| K36 DC | No token-only compression of reasoning context. |
| K37 OP | Outside: resumption protocol only if horizon/context warrants it. |
| K38 CA | No time-sensitive factual claims; runtime capability checks remain necessary. |
| K39 DC | No simulated knowledge cutoff. |
| K40 CA | No reflective optimisation loop; compare only on repeated cases with measured outcomes. |
| K41 QO | No assumption about textual gradients. |
| K42 QO | No user-memory personalisation needed. |
| K43 OP | Applied: material assumptions and unverified requirements explicit. |
| K44 QO | No uncalibrated tolerant evaluator; exact product oracle here. |
| K45 CA | No trained routing infrastructure needed. |
| K46 CA | Designer selects relevant techniques; no claim that model-selected techniques are empirically superior. |
| K47 CA | No automatic praise/feedback between turns. |
| K48 CA | Ambition, responsibility, stakes, method freedom and honest failure appear as independently justified clauses; combined motivational intervention remains experimental. |
| K49 CO | Concrete definitions and acceptance examples help fulfil the requirements; avoid claiming a universal gain. |

See `ADAPTATION_MATRIX.md` for other categories and the evaluation boundary. The knowledge base remains frozen; no new rule or research claim is introduced.
