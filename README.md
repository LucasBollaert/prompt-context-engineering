# Prompt & Context Engineering

[![Tests](https://github.com/LucasBollaert/prompt-context-engineering/actions/workflows/tests.yml/badge.svg)](https://github.com/LucasBollaert/prompt-context-engineering/actions/workflows/tests.yml)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-docs)

Design, audit and evolve prompts with the **Claude Code or Codex CLI already installed on your machine**. Describe what you need; the launcher wraps it in a prepared request, sends it once to your CLI with a specialised designer prompt, and writes the resulting prompt to a file, with its assumptions, parameters and checks listed separately.

Behind the launcher: three ready-to-use system prompts (a designer, a design auditor, an integration auditor) and an evidence-graded knowledge base on prompt and context engineering.

**Licences**: code under Apache‑2.0 (`LICENSE`); prompts, protocols, knowledge base and documentation under CC BY 4.0 (`LICENSE-docs`). See [Licences](#licences).

## Quick start
Requirements: Python 3.11+, Git, and `claude` (Claude Code) or `codex` (Codex CLI) installed and signed in.

```sh
git clone https://github.com/LucasBollaert/prompt-context-engineering.git
cd prompt-context-engineering
python pce.py check        # which CLIs are available
python pce.py              # interactive wizard
```

The wizard asks which CLI to use, the target model, and what you need the prompt for, then makes **one** call and writes:

```text
out/<date>-<name>/
  prompt.md       the prompt, ready to copy
  notes.md        recommended parameters, assumptions, open decisions, checks outside the prompt
  request.md      exactly what was sent to the CLI
  manifest.json   versions, hashes, usage and launch metadata
```

The same from the command line:

```sh
python pce.py generate --backend claude \
  --target "Claude Code on an existing Python repository" \
  --need "A prompt to fix a bug that logs users out after 5 minutes, without changing the public API. Pytest is available; no push rights."
```

Audit a prompt in a fresh session:

```sh
python pce.py audit --role design --prompt-file out/<run>/prompt.md --need "what the prompt is for"
python pce.py audit --role integration --prompt-file my_template.md --need-file need.md
```

Useful options: `--model` (passed to the CLI), `--dry-run` (write the request, call nothing), `--backend-arg` (a short list of extra CLI options that cannot widen access, such as `--effort` for Claude Code or `--skip-git-repo-check` for Codex; anything else is refused), `--out` (output folder). If the designer lacks one blocking fact, it answers `BLOCKED:` with the question to ask, and no prompt is written.

Use `generate --quick` for prompts you will use without a follow-up audit. Quick and standard generation use the same designer instructions, knowledge base access and pre-delivery checks. Both use the CLI's reasoning effort. For Claude Code, you can set it explicitly with `--backend-arg=--effort=VALUE`. Use the separate `audit` command for independent review.

Standard Claude Code generation always starts a fresh session. Quick generation can resume a session created by either mode. Claude Code keeps both kinds of generation sessions in its configuration directory. Audits always start fresh and are ephemeral, as are all Codex runs. PCE keeps a record per Claude Code generation session in `<out>/.pce-sessions/`.

To resume a session, the backend, model, extra backend arguments, designer role and CLI account must match. The session must be less than 3,600 seconds old from creation, with fewer than 150,000 measured input tokens. The measurement uses the last reported iteration's input, cache-read and cache-write tokens. PCE chooses the smallest context and breaks ties by most recent use. A concurrent run skips a locked session and tries another eligible one or starts fresh. PCE removes records and their locks after 7,200 seconds when it searches the pool. A failed resume returns code 2 after one call and discards the reserved records.

When PCE sends `--resume`, it starts the request with an explicit instruction to treat it as independent of all earlier requests and to use previously read knowledge base files as reference material. `request.md` contains the exact bytes sent to Claude Code.

Generation and audit manifests record `usage` with `input_tokens` (excluding cached input), `cache_read`, `cache_write`, `output_tokens` and `cost_usd`. Unreported values are `null`. Codex reports token counts and leaves `cost_usd` as `null`. For a resumed Claude Code session, the cost is the increase in reported cumulative dollars. A missing total or a negative difference yields `null`. When an invoked CLI fails or returns an invalid response envelope, the manifest records `status` as `backend error`, one invocation and any readable usage. Every Claude Code generation manifest records `session` with `reused`, `resumed_origin`, `age_s`, `context_tokens`, `isolation_notice`, `candidates` and `saved`. A session-pool write error after the call emits a warning and sets `saved` to `false` while the generation outputs are still written.

**What the launcher does not do**: it never retries, loops or chains runs on its own. Each run is **one invocation** of your CLI; inside it, the agent may take several internal model turns (for example to read the knowledge base), all counted against your quota. A generated prompt is a candidate: nothing is validated or deployed automatically.

**Read-only, and how it is enforced.** The request goes on standard input; the CLI runs from the repository folder.
- Claude Code uses `--tools Read,Grep,Glob` to limit the built-in tools and `--allowedTools` to pre-approve them. `--strict-mcp-config` and `--disallowedTools "mcp__*"` disable MCP. `--permission-mode dontAsk` denies calls that require approval, such as reads outside the repository. The role file replaces Claude Code's system prompt through `--system-prompt-file`.
- Codex: `codex exec --sandbox read-only`, approvals never escalated, your `config.toml` (including its MCP servers and profiles) and execpolicy rules ignored, nothing persisted. Codex has no system-prompt option: the role file is sent at the start of the message, clearly delimited. That is weaker than a real system prompt.
- Your own CLI configuration still applies where these flags do not reach (for example Claude Code hooks you defined). `python pce.py check` verifies that your CLI versions know every flag used.

## Optional launch plug

PCE launches the selected CLI directly by default. To use a launcher you trust, put this configuration in `~/.config/pce/plugs.toml` and replace the example command with your own.

```toml
launch = ["my-cli-wrapper", "--quiet"]
```

The `launch` list is prepended to the CLI argument list and executed without a shell. The launcher receives the request on standard input and runs from the repository folder. It must forward the input to the CLI and return the CLI's standard output and exit code. The read-only restrictions and the effective CLI account also depend on the launcher, so use a trusted configuration. Set `PCE_PLUGS` to choose another configuration file or set it to the empty string to disable the plug. A missing explicitly selected file, an invalid configuration or a missing launcher executable stops the run before the CLI is invoked. The manifest records `launch_plug` as a boolean.

For Claude Code, an account label is the path to a non-empty `CLAUDE_CONFIG_DIR`, or `~/.claude` by default, after user-home expansion and real-path resolution. With direct launch, PCE resolves this label itself. With a plug, PCE supplies two environment variables to the launcher for Claude Code generation.

- `PCE_RESUME_CANDIDATES` is a JSON list of objects with `session_id` and `account`. Quick generation reserves at most one eligible session per account. All entries with an unknown account (`null`) count as one group. The best available session from the most recently used account goes first, followed by the others in context and recency order. When the list has entries, the CLI argument list includes `--resume` followed by the first ID. The launcher may keep that ID if its CLI configuration owns the session, replace it with a listed ID owned by that configuration, or remove the two arguments to start fresh. It forwards all other CLI arguments and the request as received. If it removes the pair, the request still carries the isolation instruction supplied by PCE.
- `PCE_ACCOUNT_FILE` is a path in the run's temporary directory. The launcher may write the resolved account label there as a UTF-8 line. PCE uses the first non-empty line up to 4,096 characters and records `null` if the launcher supplies no valid label. PCE identifies the actual session from the returned `session_id` and uses the corresponding baseline if the session was reserved.

## Segmented profiles: mission prompts that keep their method
For recurring missions, a **profile** (TOML) defines the prompt as ordered segments:

- **fixed** segments, inserted verbatim: method, stopping rule, output contract, literal clauses. They can be read from live files, so the prompt always carries the version in force;
- one **mission** segment: the object of this particular mission, pasted by the user and inserted verbatim;
- **generated** segments, written by the designer for this mission: role and stakes, scope, success criteria, evidence expected.

The script assembles the final prompt deterministically, checks that every generated segment came back exactly once, and records the hash of each fixed segment.

```sh
python pce.py profiles
python pce.py generate --profile profils/examples/code_review.toml --mission-file mission.md --need "Review the auth refactor before release"
```

Two examples ship in `profils/examples/` (a read-only code review and an implementation task). Put your own profiles in `profils/local/`: Git ignores that folder, so private missions and paths stay on your machine. Writing a profile: [`profils/README.md`](profils/README.md). If another tool assembles the final prompt, `--body-only` returns only the generated segments.

## The three roles
Each role runs in its **own session**; two instructions are never loaded together.

| File | Role | When |
|---|---|---|
| [`SYSTEM_PROMPT.md`](SYSTEM_PROMPT.md) | Designer | Create, adapt, compare or evolve a prompt |
| [`AUDIT_CONCEPTION_SYSTEM_PROMPT.md`](AUDIT_CONCEPTION_SYSTEM_PROMPT.md) | Design auditor | Judge a prompt's quality: necessity, intent, the target's capabilities, constraints, context, cost |
| [`AUDIT_SYSTEM_PROMPT.md`](AUDIT_SYSTEM_PROMPT.md) | Integration auditor | Check that a prompt works in the system that reads it: contracts, variables, formats, permissions |

Without the launcher, paste one of these files as the system prompt (or custom instructions) of a capable model, and give it read access to `referentiel/`, `audit/` and `profils/` if you can. Input file for an audit: [`audit/CONTROLE_PROMPTS.md`](audit/CONTROLE_PROMPTS.md). A simple prompt needs no audit; two audits are never mandatory.

## Principles
- **Techniques are selected, not stacked.** Each piece of knowledge in the registry has a level: **OP** operational (applied when its conditions are met), **CO** conditional, **CA** candidate to test, **DC** discouraged under stated conditions, **QO** open question. A candidate is never presented as an established gain.
- **Proportion and stopping** ([`audit/INVARIANT_PROPORTION_ARRET.md`](audit/INVARIANT_PROPORTION_ARRET.md)). Only an established blocking defect requires a correction. Optional improvements and mere caution do not restart a cycle. Indispensable checks and real security risks are never skipped. Proportion is not minimalism: professional engineering quality and the foreseeable cost of maintenance and change are part of the result.
- **Freedom of method for the target**: a true purpose and precise criteria rather than an imposed procedure.
- **Language** ([`docs/LANGUAGE.md`](docs/LANGUAGE.md)): instructions to models in English by default, output language always stated, literal and human-facing text kept in its language, no imposed reasoning language.
- **Honesty**: distinguish verified fact, assumption and unknown; never claim a test that was not run.

## A worked example
[`docs/examples/`](docs/examples/) shows the selection at work on one fictional, hand-written mission. It is a demonstration of reasoning, not a template to prepend to every task, and not a measured result.
- [`LOG_SUMMARY_IMPLEMENTATION.prompt.md`](docs/examples/LOG_SUMMARY_IMPLEMENTATION.prompt.md): the prompt itself, as an agent would receive it.
- [`ANNOTATED_EXAMPLE.md`](docs/examples/ANNOTATED_EXAMPLE.md): why each passage is there, what stays outside the prompt (runtime, review, evaluation), and how each of the 49 registry entries was applied, kept outside or deliberately not selected.
- [`ADAPTATION_MATRIX.md`](docs/examples/ADAPTATION_MATRIX.md): how the same reasoning adapts to the 20 task categories of the knowledge base, to the template families and to PCE's three roles, plus a minimal behavioural evaluation plan.

## Repository map
```text
pce.py                              launcher (generate, audit, profiles, check)
launch/                             request templates and launcher tests
SYSTEM_PROMPT.md                    designer
AUDIT_CONCEPTION_SYSTEM_PROMPT.md   design auditor
AUDIT_SYSTEM_PROMPT.md              integration auditor
audit/                              common control protocol, proportion and stopping rule
profils/                            profile guide, project profile template, example launcher profiles
evaluations/                        manual control scenarios (not run on a model)
docs/                               language policy and its sources; examples/ worked, annotated prompt
referentiel/                        knowledge base v1.6, frozen, in French
  00_INDEX.md                       ← start here
  01 to 13                          principles, structure, techniques, models, context, security, evaluation, sources
  14                                former instruction, kept for history (do not load)
  15 to 17, research/               reviews and research notes (provenance of the choices)
  rules.yaml / rules.json           atomic rules with level of evidence
  research/knowledge_registry.yaml  knowledge registry (OP/CO/CA/DC/QO)
  scripts/, tests/                  validators and structural tests
```
The knowledge base is written in French; models read it without difficulty. Its research notes mention working archives that are not included in this repository.

## Limits
- Tests check documentary consistency and the code, **not model performance**. The scenarios in `evaluations/` are proposed, not run.
- The English instructions are a translation of the French v1.6; a translated prompt is a new version whose behaviour has not been measured.
- Model information dates from November 2026 and will age: check it when it is decisive. CLI flags can change: run `python pce.py check` after updating a CLI. The read-only setup was checked against the CLI documentation of November 2026, not yet against real runs.

## Verify locally
```sh
python -m pip install -r requirements.txt          # PyYAML, for the knowledge base scripts
python -m unittest discover -s launch/tests         # launcher tests (no model called)
python scripts_manifest.py --check                  # SHA256SUMS = exactly the files git publishes
(cd referentiel && python scripts/run_tests.py && python scripts/registry.py)
```
The same checks run on every push (Tests badge). To qualify the launcher with your real CLIs (a few invocations, after confirmation): `bash launch/qualify_cli.sh`.

## Contributing
For each proposal, state the need, the defect or hypothesis, the source, the minimal change, its validation and its limits. Instructions stay candidates until an explicit decision. Do not submit private business prompts, traces, secrets or internal archives. After a change, regenerate the hashes with `python scripts_manifest.py`.

## Licences
- Code (`pce.py`, `launch/`, `referentiel/scripts/`, `scripts_manifest.py`): Apache License 2.0, see `LICENSE`.
- Prompts, protocols, profiles, knowledge base and documentation: Creative Commons Attribution 4.0 International (CC BY 4.0), see `LICENSE-docs`.
- © 2026 Lucas Bollaert. Cited sources remain the property of their authors; see `NOTICE`.

This repository provides no empirical validation of the complete setup; see `VERIFICATIONS.md`. History: [`CHANGELOG.md`](CHANGELOG.md).
