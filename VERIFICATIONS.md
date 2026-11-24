# Verifications v1.7.1 candidate

- Knowledge base structural suite: 930 checks, 0 failures; registry: 49 valid entries.
- All knowledge base files compared byte for byte with the v1.6 scientific archive: unchanged.
- Launcher (`pce.py`): 44 automated tests with a fake backend (assembly, markers, errors, profiles, audit), including regression tests for the five defects found by the independent review (read-only command lines and refused extra options, manifest scope, strict marker parsing, single read of sources and role instructions, literal raw segments, mission object and audited prompt). The command lines follow the Claude Code and Codex documentation of November 2026; `python pce.py check` passes on Claude Code 2.1.331; real-CLI qualification passed on 24/11/2026 (Claude Code 2.1.331 and Codex CLI 0.167.0, Linux aarch64; one run per trial; free-form mode only). `launch/qualify_cli.sh` runs the real-CLI qualification (generation, refusal to write, design audit), without presenting a failed or inconclusive run as a success.
- Translation of the instructions: counter-checked independently (principles preserved).
- Targeted search for private markers and a few secret formats: no result. This check is not an exhaustive confidentiality or rights review.
- A translated prompt is a new version: its behaviour has not been measured.
- Worked example (`docs/examples/`): the ledger's 49 entries and levels checked against `research/knowledge_registry.yaml`; the classification of the example checked against `09`. Static coverage only; the example prompt was not run on a model.
- Manual scenarios documented, not run on a model. No real-reader test, launch, expenditure or publication.
