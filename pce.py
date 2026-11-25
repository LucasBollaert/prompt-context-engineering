#!/usr/bin/env python3
"""pce — generate and audit prompts with the Claude Code or Codex CLI installed on this machine.

    python pce.py                      interactive wizard
    python pce.py generate ...         generate a prompt (free-form need, or a segmented profile)
    python pce.py audit ...            audit an existing prompt (design or integration role)
    python pce.py profiles             list available profiles
    python pce.py check                show which CLIs are installed

One run = one invocation of the chosen CLI, read-only. Inside that invocation the agent may take
several internal model turns (for example to read files of the knowledge base); pce itself never
retries or loops. Outputs go to out/.
Requires Python 3.11+. Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit("pce requires Python 3.11 or later (tomllib).")
import tomllib  # noqa: E402

VERSION = "1.8.1"
ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "launch" / "templates"
ROLE_FILES = {
    "designer": ROOT / "SYSTEM_PROMPT.md",
    "design": ROOT / "AUDIT_CONCEPTION_SYSTEM_PROMPT.md",
    "integration": ROOT / "AUDIT_SYSTEM_PROMPT.md",
}
PROFILE_DIRS = [ROOT / "profils" / "examples", ROOT / "profils" / "local"]
SEG_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{0,39}$")
VAR = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")
MARKER = re.compile(r"<<<PCE:([^:<>\s]*):(BEGIN|END) ([^<>\s]*)>>>")
READ_ONLY_TOOLS = "Read,Grep,Glob"
SESSION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}")
QUICK_SESSION_MAX_AGE = 3600
QUICK_MAX_CONTEXT = 150_000
SESSION_RETENTION = 2 * QUICK_SESSION_MAX_AGE
RESUME_NOTICE = (
    "Independent request. This request has no link with any request handled earlier in this session: "
    "do not reuse, continue or refer to their needs, missions, objects, answers or wording. "
    "Knowledge-base files read earlier remain valid reference material; reread any file whose exact text you need."
)
KB_RULE = {
    False: "You may read the knowledge base in `referentiel/` (start with `referentiel/00_INDEX.md` and "
           "`referentiel/research/knowledge_registry.yaml`) when the situation calls for it. Do not load everything.",
    True: "Quick mode: consult the knowledge base in `referentiel/` when relevant. Start with "
          "`referentiel/00_INDEX.md` and `referentiel/research/knowledge_registry.yaml`, "
          "and read only what this request calls for.",
}
# Extra CLI options accepted through --backend-arg (name -> takes a value). Anything else is refused,
# because it could widen the read-only tool set, the permissions or the instructions.
BACKEND_ARGS = {
    "claude": {"--effort": True, "--max-turns": True, "--fallback-model": True},
    "codex": {"--skip-git-repo-check": False, "--oss": False},
}
# Flags pce relies on; 'check' verifies the installed CLI documents them.
REQUIRED_FLAGS = {
    # --system-prompt-file is documented but not listed by `claude --help` (2.1.331): its sibling is checked.
    "claude": ["--system-prompt", "--tools", "--allowedTools", "--disallowedTools",
               "--strict-mcp-config", "--permission-mode", "--no-session-persistence", "--output-format",
               "--resume"],
    "codex": ["--sandbox", "--ignore-user-config", "--ignore-rules", "--ephemeral",
              "--output-last-message", "--config", "--json"],
}


class PceError(Exception):
    """A user-facing error: printed without a traceback."""


# --------------------------------------------------------------------------- text helpers
def read_text(path: Path) -> str:
    """Read UTF-8 text exactly as stored (no line-ending translation)."""
    try:
        return path.read_bytes().decode("utf-8")
    except FileNotFoundError:
        raise PceError(f"file not found: {path}") from None
    except UnicodeDecodeError as e:
        raise PceError(f"{path}: not valid UTF-8 ({e})") from None


def write_text(path: Path, text: str) -> None:
    """Write UTF-8 text exactly as given (no line-ending translation, also on Windows)."""
    path.write_bytes(text.encode("utf-8"))


def fill(template: str, values: dict[str, str]) -> str:
    """Replace {{name}} placeholders. Unknown placeholders are an error."""
    def sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in values:
            raise PceError(f"unresolved placeholder {{{{{key}}}}}")
        return values[key]
    return VAR.sub(sub, template)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- profiles
def load_profile(path: Path) -> dict:
    """Load and validate a segmented profile (TOML)."""
    try:
        data = tomllib.loads(read_text(path))
    except tomllib.TOMLDecodeError as e:
        raise PceError(f"{path}: invalid TOML: {e}") from None
    w = f"profile {path.name}"
    for key in ("name", "version", "description"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise PceError(f"{w}: '{key}' must be a non-empty string")
    allowed = {"name", "version", "description", "target", "prompt_language", "variables", "segments", "notes"}
    unknown = set(data) - allowed
    if unknown:
        raise PceError(f"{w}: unknown keys {sorted(unknown)}")
    variables = data.get("variables", {})
    if not isinstance(variables, dict) or not all(isinstance(v, str) for v in variables.values()):
        raise PceError(f"{w}: [variables] must map names to strings")
    segs = data.get("segments")
    if not isinstance(segs, list) or not segs:
        raise PceError(f"{w}: at least one [[segments]] entry is required")
    seen, n_mission, n_generated = set(), 0, 0
    for s in segs:
        sid = s.get("id")
        if not isinstance(sid, str) or not SEG_ID.match(sid):
            raise PceError(f"{w}: invalid segment id {sid!r}")
        if sid in seen:
            raise PceError(f"{w}: duplicate segment id {sid!r}")
        seen.add(sid)
        kind = s.get("kind")
        extra = set(s) - {"id", "kind", "text", "file", "instruction", "heading", "raw"}
        if extra:
            raise PceError(f"{w}: segment {sid}: unknown keys {sorted(extra)}")
        if kind in ("fixed", "reference"):
            if ("text" in s) == ("file" in s):
                raise PceError(f"{w}: {kind} segment {sid} needs exactly one of 'text' or 'file'")
        elif kind == "generated":
            n_generated += 1
            if not isinstance(s.get("instruction"), str) or not s["instruction"].strip():
                raise PceError(f"{w}: generated segment {sid} needs an 'instruction'")
        elif kind == "mission":
            n_mission += 1
        else:
            raise PceError(f"{w}: segment {sid}: kind must be fixed, generated, mission or reference")
    if n_mission > 1:
        raise PceError(f"{w}: at most one mission segment")
    if n_generated == 0:
        raise PceError(f"{w}: at least one generated segment is required")
    data["_path"] = path
    return data


def fixed_raw(profile: dict, seg: dict) -> str:
    if "text" in seg:
        return seg["text"]
    p = Path(os.path.expanduser(seg["file"]))
    if not p.is_absolute():
        p = profile["_path"].parent / p
    return read_text(p)


def fixed_text(profile: dict, seg: dict, values: dict[str, str]) -> str:
    """Text of a fixed or reference segment.

    raw = true: inserted exactly as stored, character for character (no placeholder substitution,
    line endings, surrounding blank lines and final newline kept). Otherwise: {{var}} placeholders
    are replaced and leading/trailing line breaks are trimmed; line endings inside are kept.
    """
    text = fixed_raw(profile, seg)
    return text if seg.get("raw") else fill(text, values).strip("\r\n")


def load_sources(profile: dict, values: dict[str, str]) -> dict[str, str]:
    """Read every fixed and reference segment once. The run reuses exactly this data."""
    return {s["id"]: fixed_text(profile, s, values)
            for s in profile["segments"] if s["kind"] in ("fixed", "reference")}


def builtin_profile() -> dict:
    """Free-form mode: the whole prompt is one generated segment."""
    return {
        "name": "free-form", "version": VERSION, "description": "Free-form prompt request",
        "segments": [{"id": "prompt", "kind": "generated",
                      "instruction": "The complete prompt to deliver, ready to copy."}],
        "variables": {}, "_path": ROOT / "pce.py", "_builtin": True,
    }


def list_profiles() -> list[Path]:
    found = []
    for d in PROFILE_DIRS:
        if d.is_dir():
            found += sorted(d.glob("*.toml"))
    return found


# --------------------------------------------------------------------------- request building
def markers(nonce: str, sid: str) -> tuple[str, str]:
    return f"<<<PCE:{nonce}:BEGIN {sid}>>>", f"<<<PCE:{nonce}:END {sid}>>>"


def data_block(tag: str, text: str, nonce: str, attrs: str = "", keep: bool = False) -> str:
    """Delimit data. The tag carries the run nonce, so the data cannot close it early.
    keep=True: the text is shown exactly as given (only an empty text becomes a placeholder)."""
    if not keep:
        text = (text or "").strip() or "(none provided)"
    elif not text:
        text = "(none provided)"
    return f"<{tag}_{nonce}{attrs}>\n{text}\n</{tag}_{nonce}>"


def build_generate_request(profile: dict, need: str, target: str, context: str,
                           mission: str, sources: dict[str, str], nonce: str,
                           language: str, quick: bool = False) -> str:
    seg_lines, blocks, refs = [], [], []
    for s in profile["segments"]:
        if s["kind"] == "reference":
            refs.append(data_block("reference", sources[s["id"]], nonce, f' id="{s["id"]}"', keep=True))
        elif s["kind"] == "fixed":
            seg_lines.append(f"- `{s['id']}` (fixed, inserted verbatim by the script; do not rewrite or repeat it)")
            blocks.append(data_block("fixed_segment", sources[s["id"]], nonce, f' id="{s["id"]}"', keep=True))
        elif s["kind"] == "mission":
            seg_lines.append(f"- `{s['id']}` (mission object, inserted verbatim by the script)")
        else:
            b, e = markers(nonce, s["id"])
            seg_lines.append(f"- `{s['id']}` (YOU write it): {s['instruction'].strip()}\n  Wrap it exactly between `{b}` and `{e}`.")
    template = read_text(TEMPLATES / ("generate_free.md" if profile.get("_builtin") else "generate_profile.md"))
    return fill(template, {
        "profile_name": profile["name"], "profile_version": profile["version"],
        "profile_description": profile["description"].strip(),
        "target": target.strip() or profile.get("target", "") or "(not specified)",
        "prompt_language": language,
        "segments": "\n".join(seg_lines),
        "fixed_segments": "\n\n".join(blocks) or "(none)",
        "references": "\n\n".join(refs) or "(none)",
        "need": data_block("user_need", need, nonce),
        "context": data_block("user_context", context, nonce),
        "mission": data_block("mission_object", mission, nonce, keep=True),
        "profile_notes": (profile.get("notes") or "").strip() or "(none)",
        "kb_rule": KB_RULE[quick],
    })


def build_audit_request(prompt: str, need: str, target: str, context: str, nonce: str) -> str:
    return fill(read_text(TEMPLATES / "audit.md"), {
        "prompt": data_block("audited_prompt", prompt, nonce, keep=True),
        "need": data_block("original_need", need, nonce),
        "target": target.strip() or "(not specified)",
        "context": data_block("audit_context", context, nonce),
    })


# --------------------------------------------------------------------------- backends
def detect_backends() -> list[str]:
    return [b for b in ("claude", "codex") if shutil.which(b)]


def check_backend_args(backend: str, extra: list[str]) -> list[str]:
    """Accept only the extra options listed in BACKEND_ARGS (forms: --opt, --opt value, --opt=value)."""
    allowed, i = BACKEND_ARGS.get(backend, {}), 0
    while i < len(extra):
        name = extra[i].split("=", 1)[0]
        if name not in allowed:
            raise PceError(f"--backend-arg {extra[i]!r} is not allowed for {backend} "
                           f"(allowed: {', '.join(sorted(allowed)) or 'none'}); it could weaken the read-only run")
        if allowed[name] and "=" not in extra[i]:
            if i + 1 >= len(extra):
                raise PceError(f"--backend-arg {name} needs a value")
            i += 1
        i += 1
    return extra


def launch_prefix() -> tuple[str, ...]:
    config = os.environ.get("PCE_PLUGS")
    if config == "":
        return ()
    try:
        path = Path(config).expanduser() if config is not None else Path.home() / ".config" / "pce" / "plugs.toml"
    except (OSError, RuntimeError) as e:
        raise PceError(f"could not locate launch configuration: {e}") from None
    try:
        with path.open("rb") as stream:
            data = tomllib.load(stream)
    except FileNotFoundError:
        if path.is_symlink():
            raise PceError(f"{path}: launch configuration link has no target") from None
        if config is not None:
            raise PceError(f"{path}: launch configuration file not found") from None
        return ()
    except (OSError, ValueError) as e:
        raise PceError(f"{path}: could not read launch configuration: {e}") from None
    launch = data.get("launch")
    if (set(data) != {"launch"} or not isinstance(launch, list) or not launch or not launch[0]
            or any(not isinstance(arg, str) or "\x00" in arg for arg in launch)):
        raise PceError(f"{path}: expected only 'launch', a non-empty list of command strings")
    exe = shutil.which(launch[0])
    if exe is None:
        raise PceError(f"{path}: launch executable not found: {launch[0]!r}")
    return (os.path.abspath(exe), *launch[1:])


def valid_session_id(value: object) -> bool:
    return isinstance(value, str) and SESSION_ID.fullmatch(value) is not None


def backend_command(backend: str, exe: str, system_file: Path, model: str | None,
                    extra: list[str], last: Path, quick: bool = False, *, audit: bool = False,
                    resume: str | None = None, launch: tuple[str, ...] = ()) -> list[str]:
    """The exact command line. The request itself is always sent on standard input."""
    extra = check_backend_args(backend, extra)
    if backend == "claude":
        # --tools sets which built-in tools exist (read-only ones only); --allowedTools merely
        # pre-approves them. MCP tools are not covered by --tools: load none and deny any.
        # dontAsk denies every call that would need approval (e.g. reads outside the repository).
        cmd = [exe, "-p", "Answer the request given on standard input, exactly as it specifies.",
               "--system-prompt-file", str(system_file),
               "--tools", READ_ONLY_TOOLS,
               "--strict-mcp-config", "--permission-mode", "dontAsk",
               "--output-format", "json", "--allowedTools", READ_ONLY_TOOLS]
        if audit:
            cmd += ["--no-session-persistence"]
        elif quick and resume is not None:
            if not valid_session_id(resume):
                raise PceError("invalid Claude session id")
            cmd += ["--resume", resume]
        if model:
            cmd += ["--model", model]
        return [*launch, *cmd, *extra, "--disallowedTools", "mcp__*"]
    # Codex: read-only sandbox, no approval escalation, user config (MCP servers, profiles) and
    # execpolicy rules ignored, nothing persisted. The prompt "-" is read from standard input.
    cmd = [exe, "exec", "--sandbox", "read-only", "--config", 'approval_policy="never"',
           "--ignore-user-config", "--ignore-rules", "--ephemeral", "--json", "--output-last-message", str(last)]
    if model:
        cmd += ["--model", model]
    return [*launch, *cmd, *extra, "-"]


def instructions_channel(backend: str) -> str:
    if backend == "codex":
        return ("user message: Codex exec has no system-prompt option; the role file is sent first in the "
                "message, delimited (model_instructions_file would replace Codex's own base instructions; not used)")
    if backend == "claude":
        return "system prompt (--system-prompt-file, replaces Claude Code's default system prompt)"
    return "fake backend (tests)"


def snapshot_role(role_file: Path, run: Path) -> tuple[str, Path]:
    """Read the role (system) instructions once; the CLI is given this snapshot, not the live file."""
    text = read_text(role_file)
    snap = (run / f"role_{role_file.name}").resolve()   # absolute: the CLI runs from the repository
    write_text(snap, text)
    return text, snap


@dataclass
class BackendResult:
    response: str
    usage: dict[str, int | float | None]
    session_id: str | None = None
    context_tokens: int | None = None
    launch_plug: bool = False
    error: str | None = None
    account: str | None = None


def token_count(value: object) -> int | None:
    return value if type(value) is int and value >= 0 else None


def finite_number(value: object) -> bool:
    return type(value) in (int, float) and -sys.float_info.max <= value <= sys.float_info.max


def usage_fields(data: object, cache_read: str, cache_write: str) -> dict[str, int | float | None]:
    counters = data if isinstance(data, dict) else {}
    return {"input_tokens": token_count(counters.get("input_tokens")),
            "cache_read": token_count(counters.get(cache_read)),
            "cache_write": token_count(counters.get(cache_write)),
            "output_tokens": token_count(counters.get("output_tokens")),
            "cost_usd": None}


def claude_response(stdout: bytes) -> BackendResult:
    data = json.loads(stdout)
    if not isinstance(data, dict):
        data = {}
    detail = data.get("result")
    response = detail if isinstance(detail, str) else ""
    error = None
    if data.get("is_error") is not False or data.get("subtype") != "success" or not isinstance(detail, str):
        error = "claude returned an unsuccessful or invalid result" + (f":\n{response[-2000:]}" if response else "")
    counters = data.get("usage")
    usage = usage_fields(counters, "cache_read_input_tokens", "cache_creation_input_tokens")
    cost = data.get("total_cost_usd")
    if finite_number(cost) and cost >= 0:
        usage["cost_usd"] = cost
    session_id = data.get("session_id")
    iterations = counters.get("iterations") if isinstance(counters, dict) else None
    context = None
    if isinstance(iterations, list) and iterations:
        last = usage_fields(iterations[-1], "cache_read_input_tokens", "cache_creation_input_tokens")
        counts = (last["input_tokens"], last["cache_read"], last["cache_write"])
        if None not in counts:
            context = sum(counts)
    return BackendResult(response, usage, session_id if valid_session_id(session_id) else None, context, error=error)


def codex_response(stdout: bytes, last: Path) -> BackendResult:
    usage = None
    error = None
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except (ValueError, RecursionError) as e:
            error = f"codex output could not be read: {e}"
            continue
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            error = "codex returned an invalid JSON event"
        elif event["type"] == "turn.completed":
            usage = event.get("usage")
    counts = usage_fields(usage, "cached_input_tokens", "cache_write_input_tokens")
    total, cached = counts["input_tokens"], counts["cache_read"]
    counts["input_tokens"] = total - cached if total is not None and cached is not None and cached <= total else None
    response = ""
    if error is None:
        try:
            response = read_text(last)
        except PceError as e:
            error = str(e)
        except OSError as e:
            error = f"codex output could not be read: {e}"
    return BackendResult(response, counts, error=error)


def read_reported_account(path: Path) -> str | None:
    try:
        with path.open("rb") as stream:
            for line in stream:
                account = line.decode("utf-8").rstrip("\r\n")
                if account.strip():
                    return account if len(account) <= 4096 else None
    except (OSError, UnicodeDecodeError):
        pass
    return None


def run_backend(backend: str, system_file: Path, system: str, request: str, workdir: Path,
                model: str | None, extra: list[str], quick: bool = False, *, audit: bool = False,
                resume: str | None = None, launch: tuple[str, ...] | None = None,
                candidates: list[dict[str, str | None]] | None = None) -> BackendResult:
    """system_file is the run's snapshot of the role instructions; system is its text."""
    if backend == "fake":
        fake = os.environ.get("PCE_FAKE_RESPONSE_FILE")
        if not fake:
            raise PceError("fake backend: set PCE_FAKE_RESPONSE_FILE")
        return BackendResult(fill_fake(read_text(Path(fake))), usage_fields(None, "", ""))
    if launch is None:
        launch = launch_prefix()
    exe = shutil.which(backend)
    if not exe:
        raise PceError(f"'{backend}' is not installed or not on PATH (see: python pce.py check)")
    with tempfile.TemporaryDirectory(dir=workdir.resolve()) as tmp:
        last = Path(tmp) / "last.md"
        cmd = backend_command(backend, exe, system_file, model, extra, last, quick, audit=audit,
                              resume=resume, launch=launch)
        if resume is not None:
            request = f"{RESUME_NOTICE}\n\n{request}"
            write_text(workdir / "request.md", request)
        stdin = request if backend == "claude" else (
            f"<operating_instructions source=\"{system_file.name.removeprefix('role_')}\">\n{system}\n</operating_instructions>\n\n"
            f"Follow the operating instructions above for this request.\n\n{request}")
        account_file = None
        launch_options = {}
        if launch and candidates is not None:
            account_file = Path(tmp) / "account"
            launch_options["env"] = dict(os.environ, PCE_RESUME_CANDIDATES=json.dumps(candidates),
                                         PCE_ACCOUNT_FILE=str(account_file))
        # Bytes in and out: no line-ending translation of the request or the answer (Windows).
        try:
            proc = subprocess.run(cmd, input=stdin.encode("utf-8"), capture_output=True, cwd=ROOT, **launch_options)
        except OSError as e:
            raise PceError(f"could not launch {backend}: {e}") from None
        try:
            result = claude_response(proc.stdout) if backend == "claude" else codex_response(proc.stdout, last)
        except (ValueError, RecursionError) as e:
            result = BackendResult("", usage_fields(None, "", ""), error=f"{backend} output could not be read: {e}")
        if proc.returncode != 0:
            # The CLI may put its error on stdout instead of stderr.
            err = proc.stderr.strip() or proc.stdout.strip()
            result.error = f"{backend} failed (code {proc.returncode}):\n{err.decode('utf-8', errors='replace')[-2000:]}"
        if result.error is not None:
            (workdir / "response_raw.md").write_bytes(proc.stdout)
        result.launch_plug = bool(launch)
        if account_file is not None:
            result.account = read_reported_account(account_file)
        return result


_FAKE_NONCE = None


def fill_fake(text: str) -> str:
    """Tests: the fake response may use {NONCE} where the run nonce is expected."""
    return text.replace("{NONCE}", _FAKE_NONCE or "")


# --------------------------------------------------------------------------- response parsing and assembly
def extract_segments(response: str, profile: dict, nonce: str) -> tuple[dict[str, str], str]:
    """Validate the whole marker structure, then return the generated segments and the notes.

    Every marker must carry this run's nonce; markers must come in BEGIN/END pairs, unnested;
    each generated segment appears exactly once, no other id appears, and no segment is empty
    once a wrapping code fence is removed.
    """
    expected = [s["id"] for s in profile["segments"] if s["kind"] == "generated"]
    found = list(MARKER.finditer(response))
    if response.count("<<<PCE:") != len(found):
        raise PceError("malformed segment marker in the answer. Raw answer kept in the output folder.")
    out, notes, pos, open_m = {}, [], 0, None
    for m in found:
        mnonce, kind, sid = m.groups()
        if mnonce != nonce:
            raise PceError(f"marker with a foreign nonce in the answer ({m.group(0)})")
        if kind == "BEGIN":
            if open_m:
                raise PceError(f"segment '{sid}' begins inside segment '{open_m.group(3)}'")
            if sid not in expected:
                raise PceError(f"unexpected segment '{sid}' in the answer")
            if sid in out:
                raise PceError(f"segment '{sid}' was returned more than once")
            notes.append(response[pos:m.start()])
            open_m = m
        else:
            if not open_m or open_m.group(3) != sid:
                raise PceError(f"END marker for '{sid}' without its BEGIN marker")
            body = strip_fence(response[open_m.end():m.start()])
            if not body.strip():
                raise PceError(f"segment '{sid}' is empty")
            out[sid] = body
            notes.append("\n")   # the segment itself is not part of the notes
            pos, open_m = m.end(), None
    if open_m:
        raise PceError(f"segment '{open_m.group(3)}' is not closed")
    missing = [sid for sid in expected if sid not in out]
    if missing:
        raise PceError(f"the model did not return segment(s) {', '.join(missing)} (markers missing). "
                       f"Raw answer kept in the output folder.")
    notes.append(response[pos:])
    return out, "".join(notes).strip()


def strip_fence(text: str) -> str:
    """Trim surrounding line breaks and remove a single Markdown code fence wrapping the whole segment."""
    t = text.strip()
    m = re.fullmatch(r"```[A-Za-z0-9_-]*\r?\n(.*?)\r?\n?```", t, re.S)
    return (m.group(1) if m else t).strip("\r\n")


def assemble(profile: dict, generated: dict[str, str], mission: str,
             sources: dict[str, str], body_only: bool) -> str:
    """Join the segments in profile order, separated by one blank line. Fixed text comes from
    `sources` (read once per run); raw segments are inserted character for character."""
    label = body_only and sum(s["kind"] == "generated" for s in profile["segments"]) > 1
    parts = []
    for s in profile["segments"]:
        if s["kind"] == "reference":
            continue
        if s["kind"] == "generated":
            text = generated[s["id"]]
        elif body_only:
            continue
        elif s["kind"] == "fixed":
            text = sources[s["id"]]
        else:
            if not mission.strip():
                raise PceError(f"profile {profile['name']} needs a mission object (--mission-file)")
            text = mission   # inserted exactly as given
        heading = s.get("heading") or (f"## {s['id']}" if label else "")
        if heading:
            text = f"{heading}\n{text}"
        parts.append(text)
    final = "\n\n".join(parts)
    if not final.endswith("\n"):
        final += "\n"
    # Unknown {{...}} in fixed segments already failed in fill(); placeholders written by the
    # designer (e.g. a reusable template) are legitimate and kept.
    if "<<<PCE:" in final:
        raise PceError("marker residue in the final prompt")
    return final


# --------------------------------------------------------------------------- output
def new_run_dir(base: Path, label: str) -> Path:
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", label).strip("-")[:40] or "run"
    base.mkdir(parents=True, exist_ok=True)
    while True:   # two runs in the same second must not collide
        d = base / f"{stamp}-{safe}-{secrets.token_hex(2)}"
        try:
            d.mkdir()
            return d
        except FileExistsError:
            continue


def git_commit() -> str | None:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                           capture_output=True, text=True, timeout=5)
        return r.stdout.strip() or None if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_session(path: Path) -> dict | None:
    try:
        if not stat.S_ISREG(path.lstat().st_mode):
            return None
        state = json.loads(path.read_bytes())
    except (OSError, ValueError, RecursionError):
        return None
    fields = {"backend", "model", "backend_args", "role_sha256", "account", "session_id", "origin",
              "created", "last_used", "context_tokens", "total_cost_usd"}
    if not isinstance(state, dict) or not fields <= state.keys():
        return None
    if (not valid_session_id(state["session_id"]) or state["session_id"] != path.stem
            or state["origin"] not in ("standard", "quick")
            or (state["account"] is not None and not (isinstance(state["account"], str) and state["account"]))
            or not all(finite_number(state[k]) for k in ("created", "last_used"))):
        return None
    context, cost = state["context_tokens"], state["total_cost_usd"]
    if context is not None and token_count(context) is None:
        return None
    if cost is not None and not (finite_number(cost) and cost >= 0):
        return None
    return state


def replace_session(path: Path, state: dict) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".session-", delete=False) as tmp:
        temp_path = Path(tmp.name)
    try:
        temp_path.write_bytes((json.dumps(state, indent=2) + "\n").encode("ascii"))
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def session_order(state: dict) -> tuple[int, float, str]:
    return state["context_tokens"], -state["last_used"], state["session_id"]


class SessionPool:
    def __init__(self, workdir: Path):
        self.path = workdir / ".pce-sessions"
        self.owners: dict[str, bytes] = {}

    def check_path(self) -> None:
        try:
            mode = self.path.lstat().st_mode
        except FileNotFoundError:
            return
        if not stat.S_ISDIR(mode):
            raise NotADirectoryError(f"{self.path} is not a directory")

    def entry(self, session_id: str) -> Path:
        return self.path / f"{session_id}.json"

    def lock(self, session_id: str) -> Path:
        return self.path / f"{session_id}.lock"

    def claim(self, session_id: str) -> bool:
        owner = secrets.token_hex(16).encode("ascii")
        try:
            fd = os.open(self.lock(session_id), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            return False
        self.owners[session_id] = owner
        with os.fdopen(fd, "wb") as stream:
            stream.write(owner)
        return True

    def owns(self, session_id: str) -> bool:
        try:
            return self.lock(session_id).read_bytes() == self.owners[session_id]
        except FileNotFoundError:
            return False

    def release(self, session_id: str) -> None:
        if self.owns(session_id):
            self.lock(session_id).unlink(missing_ok=True)
        del self.owners[session_id]

    def discard(self, session_id: str) -> None:
        if self.owns(session_id):
            self.entry(session_id).unlink(missing_ok=True)

    def save(self, state: dict) -> bool:
        self.path.mkdir(exist_ok=True)
        session_id = state["session_id"]
        if session_id not in self.owners and not self.claim(session_id):
            return False
        if not self.owns(session_id):
            return False
        replace_session(self.entry(session_id), state)
        return True

    def reserve(self, key: dict, account: str | None, via_plug: bool, clock: Callable[[], float]) -> list[dict]:
        def eligible(state: dict, now: float) -> bool:
            return (0 <= now - state["created"] < QUICK_SESSION_MAX_AGE
                    and state["context_tokens"] is not None and state["context_tokens"] < QUICK_MAX_CONTEXT
                    and (via_plug or state["account"] == account)
                    and all(state[k] == v for k, v in key.items()))

        now = clock()
        try:
            paths = list(self.path.iterdir())
        except FileNotFoundError:
            return []
        ranked = []
        for path in paths:
            if path.suffix != ".json" or not valid_session_id(path.stem):
                continue
            state = read_session(path)
            if state is None:
                continue
            if now - state["created"] > SESSION_RETENTION:
                path.unlink(missing_ok=True)
                self.lock(state["session_id"]).unlink(missing_ok=True)
            elif eligible(state, now):
                ranked.append(state)

        reserved = []
        accounts = set()
        for state in sorted(ranked, key=session_order):
            session_id = state["session_id"]
            if state["account"] in accounts or not self.claim(session_id):
                continue
            current = read_session(self.entry(session_id))
            if current is None or not eligible(current, clock()) or current["account"] in accounts:
                self.release(session_id)
                continue
            reserved.append(current)
            accounts.add(current["account"])
            if not via_plug:
                break

        if len(reserved) > 1:
            # Prefer the account most recently used, with its lightest available session first.
            preferred = max((state for state in ranked + reserved if state["account"] in accounts),
                            key=lambda state: state["last_used"])["account"]
            reserved.sort(key=lambda state: (state["account"] != preferred, *session_order(state)))
        return reserved


def claude_account() -> str:
    config = os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude")
    return os.path.realpath(os.path.join(ROOT, config))  # The CLI runs from ROOT, including for relative config paths.


def session_warning(error: OSError) -> None:
    print(f"pce: warning: could not update Claude session pool: {error}", file=sys.stderr)


def run_generate_backend(a: argparse.Namespace, role_snap: Path, role_text: str, role_hash: str,
                         request: str, run: Path, quick: bool, *,
                         started: float, clock: Callable[[], float]) -> tuple[BackendResult, dict | None]:
    extra = a.backend_arg or []
    if a.backend != "claude":
        return run_backend(a.backend, role_snap, role_text, request, run, a.model, extra, quick), None

    launch = launch_prefix()
    pool = SessionPool(run.parent)
    key = {"backend": a.backend, "model": a.model, "backend_args": extra, "role_sha256": role_hash}
    session = {"saved": False}
    try:
        try:
            account = None if launch else claude_account()
            pool.check_path()
            reserved = pool.reserve(key, account, bool(launch), clock) if quick else []
        except OSError as e:
            raise PceError(f"could not access Claude session pool: {e}") from None
        resume = reserved[0]["session_id"] if reserved else None
        candidates = [{"session_id": state["session_id"], "account": state["account"]} for state in reserved]
        selected_at = clock()
        result = run_backend(a.backend, role_snap, role_text, request, run, a.model, extra, quick,
                             resume=resume, launch=launch, candidates=candidates if launch else None)
        state = next((entry for entry in reserved if entry["session_id"] == result.session_id), None)
        session.update(reused=state is not None, resumed_origin=state["origin"] if state else None,
                       age_s=selected_at - state["created"] if state else None,
                       context_tokens=result.context_tokens, isolation_notice=resume is not None,
                       candidates=len(candidates))
        total = result.usage["cost_usd"]
        if state:
            # Claude reports per-call tokens and cumulative dollars for a resumed session.
            previous = state["total_cost_usd"]
            result.usage["cost_usd"] = (float(Decimal(str(total)) - Decimal(str(previous)))
                                        if total is not None and previous is not None and total >= previous else None)
        if result.error is not None:
            for entry in reserved:
                try:
                    pool.discard(entry["session_id"])
                except OSError as e:
                    session_warning(e)
            if reserved:
                result.error += "\nRun again: a fresh session will be used."
        elif result.session_id is not None:
            new_state = key | {"session_id": result.session_id, "account": result.account if launch else account,
                               "origin": state["origin"] if state else ("quick" if quick else "standard"),
                               "created": state["created"] if state else started, "last_used": clock(),
                               "context_tokens": result.context_tokens, "total_cost_usd": total}
            try:
                session["saved"] = pool.save(new_state)
            except OSError as e:
                session_warning(e)
                if state:
                    # A stale context and cost baseline are unsafe after the session has advanced.
                    try:
                        pool.discard(result.session_id)
                    except OSError as discard_error:
                        session_warning(discard_error)
        return result, session
    finally:
        for session_id in tuple(pool.owners):
            try:
                pool.release(session_id)
            except OSError as e:
                session["saved"] = False
                session_warning(e)


# --------------------------------------------------------------------------- commands
def parse_vars(items: list[str]) -> dict[str, str]:
    out = {}
    for it in items or []:
        if "=" not in it:
            raise PceError(f"--var expects name=value, got {it!r}")
        k, v = it.split("=", 1)
        out[k.strip()] = v
    return out


def text_arg(value: str | None, file: str | None) -> str:
    if value and file:
        raise PceError("give the text or a file, not both")
    return read_text(Path(file)) if file else (value or "")


def cmd_generate(a: argparse.Namespace) -> int:
    global _FAKE_NONCE
    started = time.time()
    profile = load_profile(Path(a.profile)) if a.profile else builtin_profile()
    values = dict(profile.get("variables", {}))
    values.update(parse_vars(a.var))
    need = text_arg(a.need, a.need_file)
    if not need.strip() and profile.get("_builtin"):
        raise PceError("describe the need (--need or --need-file)")
    mission = text_arg(None, a.mission_file) if a.mission_file else ""
    if any(s["kind"] == "mission" for s in profile["segments"]) and not mission.strip():
        raise PceError(f"profile {profile['name']} needs a mission object (--mission-file)")
    context = text_arg(None, a.context_file) if a.context_file else ""
    language = a.prompt_language or profile.get("prompt_language") or "English for instructions to the model; keep user-facing text and literal values in their original language"
    nonce = secrets.token_hex(4)
    _FAKE_NONCE = nonce
    sources = load_sources(profile, values)   # the only read of fixed and reference files in this run
    quick = getattr(a, "quick", False)
    request = build_generate_request(profile, need, a.target or "", context, mission, sources, nonce, language, quick)
    run = new_run_dir(Path(a.out), profile["name"])
    write_text(run / "request.md", request)
    if a.dry_run:
        print(f"Dry run: request written to {run / 'request.md'} (no model called).")
        return 0
    print(f"Invoking {a.backend} once, read-only (designer role)…", file=sys.stderr)
    role_text, role_snap = snapshot_role(ROLE_FILES["designer"], run)
    role_hash = sha256(role_text)
    result, session = run_generate_backend(a, role_snap, role_text, role_hash, request, run, quick,
                                           started=started, clock=time.time)
    manifest = {
        "pce_version": VERSION, "repo_commit": git_commit(), "date": _dt.datetime.now().isoformat(timespec="seconds"),
        "backend": a.backend, "model": a.model, "cli_invocations": 1, "usage": result.usage,
        "launch_plug": result.launch_plug,
        "instructions_channel": instructions_channel(a.backend), "role_file": ROLE_FILES["designer"].name,
        "role_sha256": role_hash,
        **({"session": session} if session is not None else {}),
        "profile": profile["name"], "profile_version": profile["version"],
        "profile_file": None if profile.get("_builtin") else str(profile["_path"]),
        "fixed_segments": {s["id"]: sha256(sources[s["id"]])
                           for s in profile["segments"] if s["kind"] == "fixed"},
        "reference_segments": {s["id"]: sha256(sources[s["id"]])
                               for s in profile["segments"] if s["kind"] == "reference"},
        "body_only": a.body_only, "mode": "quick" if quick else "standard", "status": "invalid response",
    }
    if result.error is not None:
        manifest["status"] = "backend error"
        write_json(run / "manifest.json", manifest)
        raise PceError(result.error)
    response = result.response
    write_text(run / "response_raw.md", response)
    try:
        generated, notes = extract_segments(response, profile, nonce)
        blocked = {k: v for k, v in generated.items() if v.lstrip().startswith("BLOCKED:")}
        if blocked:
            manifest["status"] = "blocked"
            write_text(run / "notes.md", notes + "\n")
            for k, v in blocked.items():
                print(f"Blocked on segment '{k}': {v.strip()[len('BLOCKED:'):].strip()}")
            print(f"No prompt written. Answer the question, then run again. Details: {run}")
            return 3
        final = assemble(profile, generated, mission, sources, a.body_only)
        write_text(run / "prompt.md", final)
        write_text(run / "notes.md", notes + "\n")
        write_json(run / "segments.json", generated)
        manifest.update(prompt_sha256=sha256(final), status="candidate, not qualified")
    finally:
        write_json(run / "manifest.json", manifest)
    print(f"Prompt: {run / 'prompt.md'}\nNotes (assumptions, parameters, checks): {run / 'notes.md'}")
    return 0


def cmd_audit(a: argparse.Namespace) -> int:
    prompt = read_text(Path(a.prompt_file))
    need = text_arg(None, a.need_file) if a.need_file else (a.need or "")
    context = text_arg(None, a.context_file) if a.context_file else ""
    request = build_audit_request(prompt, need, a.target or "", context, secrets.token_hex(4))
    run = new_run_dir(Path(a.out), f"audit-{a.role}")
    write_text(run / "request.md", request)
    if a.dry_run:
        print(f"Dry run: request written to {run / 'request.md'} (no model called).")
        return 0
    print(f"Invoking {a.backend} once, read-only ({a.role} auditor, fresh session)…", file=sys.stderr)
    role_text, role_snap = snapshot_role(ROLE_FILES[a.role], run)
    result = run_backend(a.backend, role_snap, role_text, request, run, a.model, a.backend_arg or [], audit=True)
    manifest = {
        "pce_version": VERSION, "repo_commit": git_commit(), "date": _dt.datetime.now().isoformat(timespec="seconds"),
        "backend": a.backend, "model": a.model, "cli_invocations": 1, "usage": result.usage,
        "launch_plug": result.launch_plug,
        "instructions_channel": instructions_channel(a.backend), "role_file": ROLE_FILES[a.role].name,
        "role_sha256": sha256(role_text), "audited_prompt_sha256": sha256(prompt), "context_provided": bool(context.strip()),
    }
    if result.error is not None:
        manifest["status"] = "backend error"
        write_json(run / "manifest.json", manifest)
        raise PceError(result.error)
    write_text(run / "report.md", result.response)
    write_json(run / "manifest.json", manifest)
    print(f"Report: {run / 'report.md'}")
    return 0


def cmd_profiles(_: argparse.Namespace) -> int:
    found = list_profiles()
    if not found:
        print("No profile found in profils/examples or profils/local.")
    for p in found:
        try:
            pr = load_profile(p)
            print(f"{p.relative_to(ROOT)}  —  {pr['name']} {pr['version']}: {pr['description'].strip()}")
        except PceError as e:
            print(f"{p.relative_to(ROOT)}  —  INVALID: {e}")
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    print(f"pce {VERSION}, Python {sys.version.split()[0]}")
    usable = 0
    for b in ("claude", "codex"):
        exe = shutil.which(b)
        if not exe:
            print(f"- {b}: not found")
            continue
        try:
            v = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=20).stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            v = "?"
        print(f"- {b}: {exe} ({v})")
        try:
            sub = [exe, "--help"] if b == "claude" else [exe, "exec", "--help"]
            h = subprocess.run(sub, capture_output=True, text=True, timeout=20)
            missing = [f for f in REQUIRED_FLAGS[b] if f not in (h.stdout + h.stderr)]
        except (OSError, subprocess.TimeoutExpired):
            missing = ["(help unavailable)"]
        print(f"  read-only options: {'ok' if not missing else 'MISSING ' + ', '.join(missing) + ' (update the CLI)'}")
        usable += not missing
    for role, f in ROLE_FILES.items():
        print(f"- role {role}: {'ok' if f.exists() else 'MISSING'} {f.name}")
    ok = usable > 0 and all(f.exists() for f in ROLE_FILES.values())
    if not usable:
        print("No usable CLI: install or update claude or codex.")
    return 0 if ok else 1


# --------------------------------------------------------------------------- interactive wizard
def ask(question: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    ans = input(f"{question}{suffix}: ").strip()
    return ans or default


def ask_block(question: str) -> str:
    print(f"{question}\n(end with a line containing only a dot: .)")
    lines = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    return "\n".join(lines)


def wizard() -> int:
    backends = detect_backends()
    if not backends:
        raise PceError("neither 'claude' nor 'codex' was found on PATH (install one, then run: python pce.py check)")
    backend = ask(f"Backend ({'/'.join(backends)})", backends[0])
    if backend not in backends:
        raise PceError(f"unknown or missing backend: {backend}")
    action = ask("Generate a prompt or audit one? (generate/audit)", "generate")
    ns = argparse.Namespace(backend=backend, model=None, backend_arg=[], out=str(ROOT / "out"),
                            dry_run=False, context_file=None, target=None)
    if action == "audit":
        ns.role = ask("Auditor role (design/integration)", "design")
        ns.prompt_file = ask("Path of the prompt to audit")
        ns.need = ask_block("Describe the original need behind this prompt")
        ns.need_file = None
        ns.target = ask("Target model and environment", "")
        return confirm_and_run(cmd_audit, ns)
    profiles = list_profiles()
    choice = "0"
    if profiles:
        print("Profiles:\n  0. free-form (no profile)")
        for i, p in enumerate(profiles, 1):
            print(f"  {i}. {p.relative_to(ROOT)}")
        choice = ask("Choose", "0")
    ns.profile = None if choice == "0" else str(profiles[int(choice) - 1])
    ns.target = ask("Target model and environment (e.g. Claude Code on a Python repo)", "")
    ns.need = ask_block("Describe what you need the prompt for")
    ns.need_file, ns.mission_file, ns.var, ns.prompt_language, ns.body_only = None, None, [], None, False
    ns.quick = ask("Quick mode (same design process and CLI effort, skip follow-up review)? (y/N)", "n").lower().startswith("y")
    if ns.profile:
        prof = load_profile(Path(ns.profile))
        if any(s["kind"] == "mission" for s in prof["segments"]):
            mission = ask_block("Paste the mission object (inserted verbatim)")
            tmp = Path(tempfile.mkstemp(suffix=".md")[1])
            tmp.write_text(mission, encoding="utf-8")
            ns.mission_file = str(tmp)
        needed = set()
        for s in prof["segments"]:
            if s["kind"] in ("fixed", "reference") and not s.get("raw"):
                needed |= set(VAR.findall(fixed_raw(prof, s)))
        for v in sorted(needed - set(prof.get("variables", {}))):
            ns.var.append(f"{v}={ask(f'Value for {{{{{v}}}}}')}")
    return confirm_and_run(cmd_generate, ns)


def confirm_and_run(fn, ns) -> int:
    if ask("This makes one call to your CLI (it uses your quota). Continue? (y/n)", "y").lower() not in ("y", "yes", "o", "oui"):
        print("Cancelled.")
        return 1
    return fn(ns)


# --------------------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="pce", description=__doc__.split("\n\n")[0])
    p.add_argument("--version", action="version", version=f"pce {VERSION}")
    sub = p.add_subparsers(dest="cmd")

    def common(sp):
        sp.add_argument("--backend", choices=["claude", "codex", "fake"], default=(detect_backends() or ["claude"])[0])
        sp.add_argument("--model", help="model name passed to the CLI")
        sp.add_argument("--backend-arg", action="append", help="extra CLI option from a short allowlist (e.g. --effort high, --skip-git-repo-check); repeatable")
        sp.add_argument("--target", help="target model and environment of the prompt")
        sp.add_argument("--context-file", help="extra context given as data")
        sp.add_argument("--out", default=str(ROOT / "out"), help="output folder (default: out/)")
        sp.add_argument("--dry-run", action="store_true", help="write the request only; call nothing")

    g = sub.add_parser("generate", help="generate a prompt")
    common(g)
    g.add_argument("--need", help="what the prompt is for")
    g.add_argument("--need-file")
    g.add_argument("--profile", help="segmented profile (TOML); omit for free-form")
    g.add_argument("--mission-file", help="mission object inserted verbatim (profiles with a mission segment)")
    g.add_argument("--var", action="append", help="name=value for {{name}} in fixed segments (repeatable)")
    g.add_argument("--prompt-language", help="language policy for the produced prompt")
    g.add_argument("--body-only", action="store_true", help="output only the generated segments (when another tool assembles)")
    g.add_argument("--quick", action="store_true",
                   help="same design process and CLI effort, for prompts used without a follow-up audit")
    g.set_defaults(fn=cmd_generate)

    au = sub.add_parser("audit", help="audit a prompt in a fresh session")
    common(au)
    au.add_argument("--role", choices=["design", "integration"], required=True)
    au.add_argument("--prompt-file", required=True)
    au.add_argument("--need")
    au.add_argument("--need-file")
    au.set_defaults(fn=cmd_audit)

    sub.add_parser("profiles", help="list profiles").set_defaults(fn=cmd_profiles)
    sub.add_parser("check", help="show installed CLIs").set_defaults(fn=cmd_check)

    a = p.parse_args(argv)
    try:
        if not a.cmd:
            return wizard()
        return a.fn(a)
    except PceError as e:
        print(f"pce: {e}", file=sys.stderr)
        return 2
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
