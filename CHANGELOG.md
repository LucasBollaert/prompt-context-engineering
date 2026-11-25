# Public history

## 1.8.1 — candidate
- Audit coverage correction (prepared as 1.7.3 on the 1.7.2 base, applied here on 1.8.0). The audit formulation of the invariant (and the segments that carry it) asks to look, for each defect found, for the same defect and its family across the scope, then to keep examining the rest; a finding, even a blocking one, does not end the examination; occurrences outside the scope are reported as leads. An audit is complete when its scope is covered and the indispensable checks are obtained or reported as impossible. The example review method no longer repeats the family search, so the rule appears once in an assembled review prompt. One evaluation case added. Launcher code unchanged apart from its version.

## 1.8.0 — candidate
- Quick generation shares the standard designer instructions, pre-delivery checks and knowledge base access. Both modes use the CLI's reasoning effort. Quick is intended for prompts used without a follow-up audit.
- Generation and audit read the CLI's structured output and record token usage and reported cost in their manifests, including after backend failures.
- Claude Code standard generation always starts fresh and adds its session to the pool. Quick can resume a matching standard or quick session within age and context limits. Per-session locks let concurrent runs choose different sessions or start fresh. Resumed requests carry an independence instruction, and the manifest records the individual call's cost and reuse. A failed resume discards the reserved records and exits after one invocation.
- An optional user configuration can prepend a trusted launcher to the CLI command. The launcher can select a reserved session for its account or start fresh, and report the account it used. Direct launch remains the default.

## 1.7.2 — candidate
- `generate --quick` for single-use prompts at lower cost: same designer instructions, no file tools (Claude Code `--tools ""`; Codex is told not to read files), medium reasoning effort unless `--effort` is given, short notes. Recorded as `"mode": "quick"` in the manifest. The README states that `generate` never audits.

## 1.7.1 — candidate
After the real-CLI qualification of 24 November 2026 (Claude Code 2.1.331 and Codex CLI 0.167.0 on Linux aarch64: generation, refusal to write and design audit all passed).
- `notes.md` no longer starts with a `[segment …]` placeholder; it contains only the designer's notes.
- The audit request asks for paths relative to the repository root, so reports do not expose local absolute paths.

## 1.7 — candidate
- Launcher `pce.py`: generate or audit a prompt with the Claude Code or Codex CLI installed locally; interactive wizard or command line; one CLI invocation per run, no automatic loop; outputs (prompt, notes, request, manifest with hashes) in `out/`.
- Segmented launcher profiles (TOML): fixed segments inserted verbatim (including from live files), a mission object, and segments written by the designer; deterministic assembly and checks; `--body-only` when another tool assembles. Two example profiles.
- Instructions, protocol, invariant, profiles, cases and documentation translated into English; new Language section (instructions in English by default, output language stated, original language kept for literal and human-facing text, no imposed reasoning language). Knowledge base v1.6 unchanged (still in French).
- Corrections after independent review: Claude Code runs with `--tools Read,Grep,Glob`, no MCP server, `dontAsk` permissions and no saved session; Codex with a read-only sandbox, no escalation, user config and rules ignored, prompt on standard input; extra CLI options limited to a short allowlist; `check` verifies the flags and exits non-zero without a usable CLI. Strict marker parsing (run nonce, pairs, expected ids only, no empty segment after fence removal); data tags carry the run nonce. Each source file and the role instructions read once per run (the CLI receives the run's snapshot of the role file, whose hash is recorded); the mission object and the audited prompt are kept exactly; `raw = true` inserts text character for character; outputs, and the request sent to the CLI, written as bytes without line-ending translation; the role snapshot is passed by absolute path; CLI errors printed on stdout are reported. `launch/qualify_cli.sh` for real-CLI qualification, reporting each trial as PASS, FAIL, INCOMPLETE, NOT RUN or DONE (audit verdict still to read). Worked, annotated example in `docs/examples/` (prompt, rationale with the 49-entry ledger, adaptation matrix). `SHA256SUMS` lists exactly the files git publishes (`scripts_manifest.py --check`, used by CI). Labelled segments and `segments.json` in body-only mode.
- Proportion is not minimalism: the invariant, its two formulations (and the profile segments that carry them), the designer, the design auditor, the review method and the worked example now state that professional engineering quality and the foreseeable cost of maintenance and change are part of the result, without a new gate or an imposed architecture.
- README rewritten around the launcher (quick start, roles, repository map, licences at the top); continuous integration runs hash verification, knowledge base tests and launcher tests on every push.


## 1.6 — candidate
- Only an actually blocking finding requires a cycle; severity, evidence, classification and indispensable qualification are distinguished.
- Traceable downgrades, without systematic human arbitration; business rules take precedence.
- Scientific knowledge base v1.6 unchanged; no behavioural test.
## 1.5 — candidate
- Verdict threshold, bounded generic resumptions, traceable downgrades and an invariant that applies to realisation.
- Enriched manual scenarios; knowledge base unchanged; no behavioural validation.
## 1.4 — candidate
- Scientific knowledge base v1.6 frozen, with its own history.
- Three standalone roles: designer, design auditor, integration auditor.
- Imperative proportion and stopping invariant; separation of scientific evidence, requirements and options.
- Separate local profiles, manual control scenarios and preparation for publication.
- First public candidate distribution; no behavioural qualification on a model.
