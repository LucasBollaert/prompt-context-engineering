# Verifications v1.8.0 candidate

- Knowledge base structural suite: 930 checks, 0 failures; registry: 49 valid entries.
- All knowledge base files compared byte for byte with the v1.6 scientific archive: unchanged.
- Launcher (`pce.py`) automated tests cover assembly, markers, profiles, audit and the existing read-only restrictions. The 1.8 tests use synthetic CLI responses to check quick-mode parity, structured output, usage accounting, Claude Code session eligibility and contention, failure after resume, and the optional launch plug. The launcher suite also runs with a temporary home and an active plug that would fail if invoked during the existing tests.
- The 24 November 2026 real-CLI qualification covered 1.7 free-form generation, refusal to write and design audit with Claude Code 2.1.331 and Codex CLI 0.167.0. The 1.8 automated tests use stand-ins. Model behaviour on reused sessions and the cost of quick generation with knowledge base reads still need to be measured.
- Translation of the instructions: counter-checked independently (principles preserved).
- Targeted search for private markers and a few secret formats: no result. This check is not an exhaustive confidentiality or rights review.
- A translated prompt is a new version: its behaviour has not been measured.
- Worked example (`docs/examples/`): the ledger's 49 entries and levels checked against `research/knowledge_registry.yaml`; the classification of the example checked against `09`. Static coverage only; the example prompt was not run on a model.
- Manual scenarios documented, not run on a model. No real-reader test, launch, expenditure or publication.
