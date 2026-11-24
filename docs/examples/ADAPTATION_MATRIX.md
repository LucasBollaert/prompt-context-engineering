# Adaptation across mission types

**PCE v1.7 candidate — static educational coverage, not behavioural qualification.** Use the six axes from `referentiel/09_TASK_CLASSIFICATION.md`, the orthogonal modules, and the selective triggers in `referentiel/10_PROMPT_GENERATION_PROTOCOL.md`. T0–T3 describes complexity/horizon, not importance or permission. The snippets are illustrative additions or replacement clauses, not complete production prompts. Confirm source identities, permissions, readers and actual acceptance criteria before use. No new gate is introduced.

## Twenty categories of the frozen reference (§2.1–2.20)

| # / category | Illustrative adaptation of the worked example or a comparable task | Retain / remove and rationale |
|---|---|---|
| 2.1 Simple question | “What does WARN mean in this log format? Answer in English in one sentence.” | T0, direct request; no expert persona, audit loop, autonomy contract or artificial effort. Add a source line only if needed. |
| 2.2 Documentary research | “Compare the documented severity definitions in the current primary sources; cite dates and passages, state what differs, stop once the specified question is answered.” | Sources, freshness and stopping; remove implementation permission and code test requirements. Corroborate contested claims with independent sources when warranted. |
| 2.3 In-depth analysis | “Using the supplied log and service timeline, distinguish observed facts, plausible causes and competing hypotheses; cite evidence and limitations.” | Method freedom, assumptions and traceability; no forced framework or unsupported numeric confidence. |
| 2.4 Problem solving | “Find a way to count the two severities exactly under these constraints; verify with the provided input/output cases.” | Oracle, freedom, exact tools; no write authority unless granted. |
| 2.5 Programming | Use `LOG_SUMMARY_IMPLEMENTATION.prompt.md`. | Scoped ownership, invariants, tests, anti-overengineering, honest terminal states. |
| 2.6 Debugging | “Reproduce the duplicate ERROR count with the supplied fixture; investigate the cause and related cases; demonstrate red then green and run non-regression checks.” | Actual symptom and identity, root cause, scoped changes; remove speculative protections. |
| 2.7 Technical audit | “Review the specified change at its identified revision, read-only; inventory obligations, establish each finding with location, consequence and evidence. Record unexamined areas. Stop once the scope is covered and the indispensable checks are obtained or reported as impossible.” | Audit invariant instead of realisation; design and code quality findings count, with their concrete cost; no edits, no tests with side effects unless specifically authorised. Blind review excludes previous leads. |
| 2.8 Security audit | “Review the agreed threat model and trust boundaries for the identified log parser. Treat log data as untrusted; establish realistic paths and consequences from evidence; no production actions or unauthorised reproduction.” | Threat model and scope; real security defects matter, precautions alone do not block. No promise of absolute exhaustiveness. |
| 2.9 Architecture | “Compare viable designs for the stated throughput, latency, maintenance and compatibility needs. Explain trade-offs against the criteria and identify the closest alternative if a requirement is infeasible.” | Free exploration and owner decision; no premade options if the mission is open solution search. No speculative pre-code gates. |
| 2.10 Complete project | “Implement the approved specification incrementally; maintain the authorised progress and acceptance records, verify end-to-end criteria, and provide a resumable terminal report.” | T3, state, ownership, scope, E2E oracle, checkpoints; no universal budget or commit authority. |
| 2.11 Maintenance | “Make only the agreed change; preserve existing interfaces and conventions; verify the suite and review the diff.” | Minimal scope, non-regression, no blanket ownership or opportunistic refactoring. |
| 2.12 Data analysis | “Using the supplied schema and metric definitions, compute counts in code, reconcile totals and explain exclusions and uncertainty.” | K15 exact tool, data provenance and checks; no guessed numbers or unnecessary loading of huge tables. |
| 2.13 Decision support | “Compare the options against the owner's criteria, state assumptions and sensitivity, and recommend without making the decision on their behalf.” | Evidence, genuine stakes, human authority. No invented weights or false consensus. |
| 2.14 Documentation | “Document the supported interface for on-call engineers from the identified code/spec; verify examples if authorised; state what remains unverified.” | Audience, truth sources, language and verification; no code edit authority by implication. |
| 2.15 Creative task | “Propose three clearly different explanations of the alert display for new users, preserving required facts; vary metaphor and tone. Output in English.” | Real creative intent, flexibility and human selection; no code oracle, rigid audit or assumed benefits of persona/multilingual sampling. Candidate diversity methods may be compared when useful. |
| 2.16 Autonomous execution | “Within the explicitly allowed workspace, complete approved criteria; persist state and proofs before resumption; stop with the contract's success/partial/blocked/resource state.” | T3, actual permissions, evidence and external stop mechanisms if available. No automatic action outside scope. |
| 2.17 Multi-agent coordination | “Assign independent, bounded subtasks with distinct ownership, available tools and return contracts. Integrate evidence and deduplicate findings.” | Separate agents, isolation of writes, genuine independent review when needed; no same-model debate assumed superior. |
| 2.18 Supervision | “Check actual artefacts and evidence against the agreed acceptance conditions. Detect recurrence, drift and false success; use only the authorised next actions and escalation.” | Supervisory role does not redo work, invent gates, or relaunch automatically. |
| 2.19 Deliverable validation | “In a fresh context, compare this exact deliverable to its source requirements and acceptance evidence; distinguish omissions and defects from optional changes.” | K18, object identity, no producer conclusions; no arbitrary score or perfection loop. |
| 2.20 Incident investigation | “Build the timeline from identified logs and metrics, distinguish correlation from cause, test competing explanations within read-only permissions, recommend next steps without executing production remediation.” | Evidence and explicit scope; real incident stakes, no fake urgency or production actions. |

## Additional template families in `11_PROMPT_TEMPLATES.md`

| Family | Adaptation |
|---|---|
| T0 / T1 / T2 / T3 | Use the classification axes; preserve the direct request for the fast path when permitted, add only relevant modules for T1, use scoped autonomy for T2, persistence and terminal outcomes for T3. |
| Fresh-context reviewer | Give the exact artefact, original requirements and legitimate evidence, not the producer's conclusions in blind mode. |
| Sub-agent brief | Independent objective, scope, allowed tools, return contract and stopping conditions; supervisor owns synthesis. |
| Structured extraction | Exact schema, allowed values, missing-value behaviour and real reader; deterministic validation outside the prompt. No free-form report if the reader cannot accept it. |
| Interview / spec-first | Clarify the materially different interpretations before expensive work; not a default questionnaire. |
| Existing-prompt optimisation | Preserve the original need, compare to direct request or previous version; change only the justified cause and measure regressions. |
| Persistent instructions (CLAUDE.md, AGENTS.md, SKILL.md, sub-agent) | Stable facts and conventions only; keep variable task facts out, verify loading mechanism and precedence. Never assume a file grants authority. |

## Public profiles and PCE's three roles

The current `code_review.toml` contains generated role/scope, literal mission and fixed method/stopping/report blocks. Use the audit adaptation above, not the developer formulation. `implementation.toml` contains generated goal/criteria, literal mission and fixed realisation/report blocks. Use the worked implementation as the conceptual example. A `reference` is shown only to the designer by the assembler, never directly inserted; generated text can nevertheless quote it, so review material that must not be disclosed. Comments and this matrix stay outside the target prompt. The shipped profiles need real model/reader qualification before relying on their outputs.

| PCE role | How the example is used |
|---|---|
| Designer (`SYSTEM_PROMPT.md`) | Select the relevant clauses and justify inclusions/omissions in notes outside the prompt. Preserve the original request, fixed clauses and actual capabilities. |
| Design auditor (`AUDIT_CONCEPTION_SYSTEM_PROMPT.md`) | Independently examine necessity, method freedom, ambition, scientific applicability, fidelity and proportion; no execution of the mission. |
| Integration auditor (`AUDIT_SYSTEM_PROMPT.md`) | Independently check actual input, reader, identity, permission, failure states and workflow. A correct-looking format does not qualify a real reader. |

## Minimal behavioural evaluation plan (optional after CLI qualification)

Use the existing protocol (`referentiel/12_EVALUATION_PROTOCOL.md`). Do not launch automatically. Compare a direct request to the PCE-produced prompt with equal task information and permissions for causal comparisons; for product-level comparison record information and cost differences explicitly. Use the same target/version/effort/tools, fixtures and oracle; judge without knowing the variant when feasible; record repeats, variation, token/time/cost to accepted output, and failures. Compare representative categories first: a simple request (avoid overhead), a scoped implementation (tests), an independent audit (known defects and harmless precautions), a literal machine-contract case (real parser), and an ambiguous or blocked task (no false success). Add a long-horizon case only if it is needed. Record skipped categories as unmeasured; static adaptation above is not evidence of model behaviour. For changed prompts or target models, test relevant regressions and paraphrases. No automatic retries, expenses, or edits of the reference.
