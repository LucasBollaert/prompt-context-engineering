# Public history

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
