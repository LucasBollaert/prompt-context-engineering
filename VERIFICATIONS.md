# Verifications v1.8.1 candidate

- Knowledge base structural suite: 930 checks, 0 failures; registry: 49 valid entries.
- All knowledge base files compared byte for byte with the v1.6 scientific archive: unchanged.
- The launcher suite has 82 automated tests, including 36 in `test_pce18.py`. They cover assembly, markers, profiles, audit and the read-only restrictions. The 1.8 tests use synthetic CLI responses to check command and reasoning-effort parity, structured output, usage accounting after success and failure, session selection and contention in two concurrent threads, exact isolation request bytes, and the launcher's account and session selection contract. The full suite also runs with a temporary home and a default plug that would fail if invoked.
- Audit coverage correction (1.8.1): a `--dry-run` of the example review profile with synthetic data puts the coverage rule and the audit completion condition exactly once in `request.md`, and the former method sentence no longer appears (also an automated test). A private audit profile kept outside the repository was checked the same way. The behaviour of auditors under the new wording has not been measured.
- The 24 November 2026 real-CLI qualification covered 1.7 free-form generation, refusal to write and design audit with Claude Code 2.1.331 and Codex CLI 0.167.0. The 1.8 automated tests use stand-ins. Model behaviour on reused sessions and the cost of quick generation with knowledge base reads still need to be measured.
- Translation of the instructions: counter-checked independently (principles preserved).
- Targeted search for private markers and a few secret formats: no result. This check is not an exhaustive confidentiality or rights review.
- A translated prompt is a new version: its behaviour has not been measured.
- Worked example (`docs/examples/`): the ledger's 49 entries and levels checked against `research/knowledge_registry.yaml`; the classification of the example checked against `09`. Static coverage only; the example prompt was not run on a model.
- Manual scenarios documented, not run on a model. No real-reader test, launch, expenditure or publication.
