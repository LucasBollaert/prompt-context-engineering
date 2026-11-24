# Prompt control — common protocol v1.7 candidate

## Choosing the level of control
Internal review at every delivery (short for a simple request). A separate audit is recommended for a persistent prompt, a shared or assembled template, a machine reader, a high-stakes action, a substantial change or an observed regression. An audit can be requested at any time. For an integrated system, respect the gates and cycles actually approved: this protocol creates no additional gate or business type.

## Choosing the auditor
| Auditor | Instruction | Subject | When |
|---|---|---|---|
| Design | `AUDIT_CONCEPTION_SYSTEM_PROMPT.md` | Quality of the prompt as design: necessity, intent, native capability, ambition, constraints, context, wording and language, output, exploration, cost; use of knowledge according to its level | Any prompt, any project |
| Integration | `AUDIT_SYSTEM_PROMPT.md` | Conformity with the system: contracts, real readers, variables, states, gates, cycles, decisions | A prompt assembled, executed or read by a machine, or subject to business rules |

A prompt embedded in a system may receive both audits, in separate sessions. In blind mode, neither receives the other's conclusions. This separation reduces the influence of previous reports; it guarantees neither the statistical independence of the judgements nor the absence of shared biases. The designer then reconciles their findings. A favourable design audit does not qualify integration, and vice versa. Both check the safety and fidelity baseline applicable to their subject; do not make both audits systematic. If both dimensions are indispensable, neither can be deemed covered by the other audit alone. The launcher (`python pce.py audit`) runs each audit in a fresh process.

## Input file
- Original need, requirements and preferences, validated decisions and non-goals.
- Exact prompt, version, parameters, modules and variables; relevant assembled examples if available; SHA only if established.
- Target and environment (model, harness, tools, permissions, context, readers, contracts, oracles). Declare the unknowns.
- Applicable business profile and sources, v1.6 knowledge base; any observed behaviour, without disclosing other auditors' conclusions in a blind audit.
- For a targeted resumption only: authorised findings, targets and diff; qualify the scope of the resumption.

## Selective grid (not a checklist imposed on the prompts produced)
| Axis | Control question | Documentary basis |
|---|---|---|
| Intent | Result, requirements, preferences, non-goals and decisions preserved? | USER_REQUIREMENTS, original need, R-GEN-002 |
| Target | Model, tools, parameters and format supported? | `04`, R-CAP-001 |
| Capabilities | Precise objective and criteria; suitable autonomy, ambition, native reasoning and initiative? Procedure justified? | `06`, `14`, R01/R04 |
| Techniques | Applicable OP knowledge respected or departure justified, useful CO considered, CA reported if relevant, DC bounded? Claimed gains supported? | `03`, registry, R01–R04 |
| Intellectual independence | Presuppositions, sycophancy, alternatives and diversity where useful? | R02, registry |
| Language | Output language stated; literal values and human-facing texts kept in their language; no reasoning language imposed without reason? | `SYSTEM_PROMPT.md` (Language) |
| Context | Authorised and up-to-date sources, provenance, sufficient context, resumption/compaction, no pollution? | `05`, `07`, registry |
| Security | Permissions, actions, secrets, untrusted content, isolation and approvals; fail closed if a critical invariant is at stake? | `07`, R-SEC-* |
| Reliability | Oracle, evidence, authorised tests, reasoned stop and resumption, no fictitious success? | `06`, `07`, K31 |
| Contract | Exact inputs, variables, order, delimiters, values and states, real reader and hand-off? | real contract, business profile |
| Proportionality | Density, redundancy, total costs, suitable checks; legitimate requirements intact? | R-STR-009, `05`, `12` |
| Maintenance | Version, sources, dependencies, parameters, regressions, history, reproducibility? | README, profile, `12` |

For an integrated project, consult `profils/README.md`, the applicable profile and the real contracts; check the qualification of interfaces against their active sources. Documents of the knowledge base are written in French.

**Checking the transfer of business lessons.** Consult the applicable business profile. Check, on the final prompt and the relevant assemblies, that the requirements applicable to the role actually reach the target (text, accessible context or verified control), without injecting tasks that belong to supervision. The designer makes the essential mappings and limits visible outside the prompt; each auditor checks its own dimension. A citation in a documentary folder is not enough.

## Levels of evidence and verdict
- Static review: content, sources actually read, correspondences and contradictions. A plausible prompt is not proof of performance.
- Contract: authorised trial on the real reader, with valid and invalid cases (missing variables, delimiter characters, error states, truncated outputs where relevant). Record command, version, output and exit code. If not executed, say so.
- Behaviour: authorised trials on the real target and environment, comparison with a baseline (direct request, minimal prompt or previous version), criteria set before the trials, total cost; consult `12` for an empirical conclusion. No paid campaign without agreement.

Severity: critical, major, moderate or minor according to the established impact. Blocking status is separate: in the generic framework, an established defect that prevents a required result, a safe use or an indispensable conformity; apply the business classification if one exists. Separate options and assumptions. Generic static verdict: **corrections required** only for an established blocking finding that remains to be dealt with according to the applicable requirements, evidence and rules for moving on; severity alone is not enough; **inconclusive** for any indispensable examination not performed or unresolved critical risk that prevents qualification; **favourable** if none of these obstacles remains. All non-blocking findings, even major ones, are recorded without a dedicated cycle. Their cumulative effect may constitute a separate blocking finding if the scenario and the evidence establish it. Declare established defects and inconclusive dimensions separately. This threshold changes neither the classification nor the verdicts of approved business procedures. Declare contract and behaviour separately: not applicable / not tested / conforming or non-conforming to the defined trials / inconclusive. Never equate a favourable static verdict with ready to launch. No arbitrary numerical scoring.

## Report (human format by default)
Subject/version, mode (internal, independent blind, adversarial or resumption), sources and coverage, static verdict and justification, state of technical and behavioural validations. For each finding: ID, severity, blocking or not, qualification (established defect/plausible risk), location, requirement or evidence, impact, minimal correction, resolution test. Then optional items and limits. If nothing significant: say so. Respect the business report contract if one is provided; this human format is not inserted into a business output format or a parser without authorisation.

## Proportion and stopping invariant
`audit/INVARIANT_PROPORTION_ARRET.md` is imperative within its scope. Both auditors and the designer apply it and check that it is transmitted to the final prompt of the missions concerned. Separate scientific knowledge (level of evidence and transfer), validated operational requirements (mandatory within their scope) and options. A precaution alone does not prevent an authorised step and does not trigger a cycle. Essential prerequisites, established defects, unresolved critical risks and approved business rules are not neutralised. The absence of an option or of an experimental technique is not a blocking finding.

## Arbitration and stopping
The designer judges the findings against the sources (correct, to be qualified, wrong); the owner validates changes of scope and promotion. Keep the initial prompt, the report, the decisions, the diff and the consolidated version. Any downgrade of a blocking finding is traceable: identifier, initial classification, justification, evidence of resolution or counter-evidence, and decision. Without sufficient evidence, keep the initial finding; escalate to the person in charge only the disagreements that actually prevent moving on or require their decision. Apply the business downgrade rules where they exist, without instituting systematic human arbitration. Outside a business procedure, a correction leads at most to one targeted resumption on the corrected points and their regressions; no automatic new full audit. If a significant obstacle persists or a change substantially alters the mandate, submit the precise question and the options to the owner, without automatic promotion. Approved business procedures take precedence. Stop when the conditions of the step are met; an indispensable validation not performed forbids the qualification that depends on it. A new lead without identified impact does not trigger new research.
