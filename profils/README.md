# Profiles

This repository contains no private business data. Profiles come in two forms:

- **Project profile** (`MODELE_PROFIL.md`): a written description of your project's requirements, readers, gates and lessons, for the designer and the auditors to consult. Keep real ones outside the public repository.
- **Launcher profile** (`*.toml`): a segmented template that `pce.py` assembles into a mission prompt. Examples are in `examples/`; put your own in `profils/local/`, which Git ignores.

A profile does not replace the scientific knowledge. Do not make one project's requirements universal. No profile is needed for a simple request.

## Writing a launcher profile
A launcher profile is an ordered list of segments:

| `kind` | Written by | Inserted |
|---|---|---|
| `fixed` | You (`text = "..."` or `file = "path"`; relative to the profile, `~` allowed) | Verbatim. `{{name}}` is filled from `[variables]` or `--var name=value`; an unknown name is an error. Without `raw`: line breaks at the start and end are trimmed. With `raw = true`: inserted **character for character** (no placeholder substitution, line endings, blank lines and final newline kept), for clauses another tool or a business reader relies on. |
| `mission` | The user, at run time (`--mission-file`) | Exactly as given, line breaks included. At most one per profile. |
| `generated` | The designer model, following `instruction` | Between markers the script checks: every marker must carry the run nonce, each segment appears exactly once, unknown, nested, unclosed, duplicated or empty segments are errors. |
| `reference` | You (`text` or `file`) | Never. Shown to the designer as guidance (style guide, project rules, lessons); its hash is recorded. |

Optional keys: `heading` (a line placed before the segment), profile-level `target`, `prompt_language` and `notes` (passed to the designer). Run `python pce.py profiles` to validate the profiles you have.

Use `fixed` for everything that must not be paraphrased: output contracts, literal clauses, stopping rules, security boundaries. Point `file` at the live source of a clause rather than copying it, so the prompt always carries the version in force; the run manifest records the hash of every fixed segment. If another tool assembles the final prompt, use `--body-only` to get only the generated segments; when there are several, each one is preceded by its `heading` or by `## <id>`. Every run also writes `segments.json` (segment id → text).

Each file of a run, including the role instructions, is read **once**: the designer sees, the prompt contains and the manifest hashes exactly the same text, even if a source changes during the run. Separators between segments are one blank line; the files keep the line endings of their sources.

**Profiles are trusted configuration.** A profile can read any file you can read (`file = "~/..."`), and its text reaches the model. Use only profiles you wrote or reviewed, like a script.

**What the nonce does, and does not do.** Each run draws a random nonce used in the segment markers and in the tags around user data, so a pasted text cannot forge a segment boundary or close a data block early. It does not stop instructions hidden in that data from influencing the model: the designer is told to treat it as data, and you still review the result.
