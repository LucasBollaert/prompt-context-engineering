"""Launcher 1.8 contracts. All CLI responses are synthetic."""
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ["PCE_PLUGS"] = ""
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import pce  # noqa: E402


def answer(request):
    marker = re.search(rb"<<<PCE:([0-9a-f]+):BEGIN prompt>>>", request)
    if not marker:
        return "Audit verdict."
    nonce = marker[1].decode()
    return f"<<<PCE:{nonce}:BEGIN prompt>>>\nSynthetic prompt.\n<<<PCE:{nonce}:END prompt>>>"


def claude_result(request, *, session="session-one", cost=0.25, tokens=12,
                  context=(4, 100, 20), **fields):
    usage = {"input_tokens": 3, "cache_read_input_tokens": 100,
             "cache_creation_input_tokens": 20, "output_tokens": tokens}
    if context is not None:
        usage["iterations"] = [
            {"input_tokens": 400000, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
            dict(zip(("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"), context)),
        ]
    return {"result": answer(request), "session_id": session, "total_cost_usd": cost,
            "is_error": False, "subtype": "success", "usage": usage} | fields


class BackendTest(unittest.TestCase):
    def setUp(self):
        test_root = ROOT / "out"
        test_root.mkdir(exist_ok=True)
        tmp = tempfile.TemporaryDirectory(dir=test_root)
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name)
        self.out = self.home / "runs"
        self.out.mkdir()
        self.bin = self.home / "bin"
        self.bin.mkdir()
        self.prompt = self.home / "prompt.md"
        self.prompt.write_text("Example prompt.\n", encoding="utf-8")
        self.executables = {}
        for name in ("claude", "codex", "launcher"):
            stub = self.bin / (f"{name}.exe" if os.name == "nt" else name)
            stub.touch()
            stub.chmod(0o755)
            self.executables[name] = str(stub)
        self.plugs = self.home / ".config" / "pce" / "plugs.toml"
        self.plugs.parent.mkdir(parents=True)
        self.calls = []
        self.reply = lambda request, argv: self.json_reply(claude_result(request))
        self.now = 2_000_000_000.0
        self.enterContext(patch.dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home),
                                     PATH=str(self.bin), PCE_PLUGS=""))
        self.enterContext(patch.object(pce, "time", create=True))
        pce.time.time.side_effect = lambda: self.now
        self.enterContext(patch.object(pce, "git_commit", return_value=None))
        self.enterContext(patch.object(pce.subprocess, "run", side_effect=self.dispatch))

    def dispatch(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        return self.reply(kwargs["input"], argv)

    def json_reply(self, obj):
        return subprocess.CompletedProcess([], 0, json.dumps(obj).encode(), b"")

    def call(self, label, *options, backend="claude", audit=False):
        action = ["audit", "--prompt-file", str(self.prompt), "--role", "design"] if audit else ["generate"]
        argv = [*action, "--backend", backend, "--need", label, "--out", str(self.out), *options]
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            code = pce.main(argv)
        run, = (path for path in self.out.iterdir() if path.is_dir()
                and f"\n{label}\n" in (path / "request.md").read_text(encoding="utf-8"))
        return code, err.getvalue(), run

    def ok(self, label, *options, **kwargs):
        code, error, run = self.call(label, *options, **kwargs)
        self.assertEqual(code, 0, error)
        return run

    def manifest(self, run):
        return json.loads((run / "manifest.json").read_text(encoding="utf-8"))

    def codex_reply(self, request, argv, *, usage=None, last=True, stdout=None):
        if last:
            path = Path(argv[argv.index("--output-last-message") + 1])
            path.write_text(answer(request), encoding="utf-8")
        if stdout is None:
            stdout = (json.dumps({"type": "thread.started"}) + "\n"
                      + json.dumps({"type": "turn.completed", "usage": usage}) + "\n").encode()
        return subprocess.CompletedProcess([], 0, stdout, b"")


class Quick(unittest.TestCase):
    def test_outils_effort_et_role(self):
        role = pce.ROLE_FILES["designer"]
        for backend in ("claude", "codex"):
            with self.subTest(backend=backend):
                args = (backend, backend, role, None, [], Path("last.md"))
                quick = pce.backend_command(*args, quick=True)
                normal = pce.backend_command(*args)
                if backend == "claude":
                    for flag in ("--tools", "--allowedTools"):
                        self.assertIn(flag, quick)
                        self.assertEqual(quick[quick.index(flag) + 1], "Read,Grep,Glob")
                    self.assertEqual(quick[quick.index("--effort") + 1], "medium")
                    self.assertEqual(normal[normal.index("--effort") + 1], "medium")
                    self.assertEqual(quick[quick.index("--system-prompt-file") + 1], str(role))
                else:
                    self.assertEqual(quick, normal)
                    self.assertIn('model_reasoning_effort="medium"', normal)
        profile = pce.builtin_profile()
        args = (profile, "Need", "", "", "", {}, "1234", "English")
        quick = pce.build_generate_request(*args, quick=True)
        normal = pce.build_generate_request(*args)
        self.assertIn("Quick mode", quick)
        self.assertEqual(quick.replace(pce.KB_RULE[True], pce.KB_RULE[False]), normal)
        for entry in ("referentiel/00_INDEX.md", "referentiel/research/knowledge_registry.yaml"):
            self.assertIn(entry, quick)
        self.assertNotIn("Do not read files", quick)


class Sortie(BackendTest):
    def test_claude_result(self):
        run = self.ok("Generate A")
        self.assertEqual((run / "prompt.md").read_text(encoding="utf-8"), "Synthetic prompt.\n")
        run = self.ok("Audit A", audit=True)
        self.assertEqual((run / "report.md").read_text(encoding="utf-8"), "Audit verdict.")
        for argv, _ in self.calls:
            self.assertEqual(argv[argv.index("--output-format") + 1], "json")

    def test_claude_refuse_enveloppe_invalide(self):
        variants = {
            "error flag": b'{"is_error":true,"subtype":"success","result":"x"}',
            "error subtype": b'{"is_error":false,"subtype":"error","result":"x"}',
            "missing subtype": b'{"is_error":false,"result":"x"}',
            "missing result": b'{"is_error":false,"subtype":"success"}',
            "non-text result": b'{"is_error":false,"subtype":"success","result":[]}',
            "malformed json": b'{"result":\xff',
        }
        for label, raw in variants.items():
            with self.subTest(label=label):
                self.reply = lambda req, argv: subprocess.CompletedProcess([], 0, raw, b"")
                code, error, run = self.call(label, audit=True)
                self.assertEqual(code, 2, error)
                self.assertEqual((run / "response_raw.md").read_bytes(), raw)
                self.assertFalse((run / "report.md").exists())

    def test_codex_dernier_message_et_echec(self):
        self.reply = self.codex_reply
        run = self.ok("Codex audit", backend="codex", audit=True)
        self.assertEqual((run / "report.md").read_text(encoding="utf-8"), "Audit verdict.")
        self.assertIn("--json", self.calls[-1][0])
        raw = b'{"type":"turn.completed"}\n'
        self.reply = lambda req, argv: self.codex_reply(req, argv, last=False, stdout=raw)
        code, error, run = self.call("Codex missing message", backend="codex", audit=True)
        self.assertEqual(code, 2, error)
        self.assertEqual((run / "response_raw.md").read_bytes(), raw)
        self.assertFalse((run / "report.md").exists())

        raw = b'{"type":"thread.started"}\nnot JSON\n'
        self.reply = lambda req, argv: self.codex_reply(req, argv, stdout=raw)
        code, error, run = self.call("Codex invalid JSONL", backend="codex", audit=True)
        self.assertEqual(code, 2, error)
        self.assertEqual((run / "response_raw.md").read_bytes(), raw)

    def test_rc_non_nul_garde_la_sortie(self):
        raw = b"CLI output\r\n"
        self.reply = lambda req, argv: subprocess.CompletedProcess([], 7, raw, b"CLI failure")
        code, error, run = self.call("Failed generation")
        self.assertEqual(code, 2)
        self.assertIn("CLI failure", error)
        self.assertTrue((run / "response_raw.md").exists())
        self.assertEqual((run / "response_raw.md").read_bytes(), raw)


class Cout(BackendTest):
    def test_claude_generation_et_audit(self):
        for audit in (False, True):
            with self.subTest(audit=audit):
                run = self.ok(f"Claude usage {audit}", audit=audit)
                expected = {"input_tokens": 3, "cache_read": 100, "cache_write": 20,
                            "output_tokens": 12, "cost_usd": 0.25}
                self.assertEqual(self.manifest(run).get("usage"), expected)

    def test_codex_compte_le_cache_une_fois(self):
        usage = {"input_tokens": 120, "cached_input_tokens": 80, "cache_write_input_tokens": 0,
                 "output_tokens": 8, "reasoning_output_tokens": 3}
        self.reply = lambda req, argv: self.codex_reply(req, argv, usage=usage)
        for audit in (False, True):
            with self.subTest(audit=audit):
                run = self.ok(f"Codex usage {audit}", backend="codex", audit=audit)
                expected = {"input_tokens": 40, "cache_read": 80, "cache_write": 0,
                            "output_tokens": 8, "cost_usd": None}
                self.assertEqual(self.manifest(run).get("usage"), expected)

    def test_compteurs_absents_et_zero(self):
        expected = dict.fromkeys(("input_tokens", "cache_read", "cache_write", "output_tokens", "cost_usd"))
        self.reply = lambda req, argv: self.json_reply(
            {"result": answer(req), "subtype": "success", "is_error": False,
             "usage": {"output_tokens": 0}})
        run = self.ok("Partial Claude usage", audit=True)
        self.assertEqual(self.manifest(run).get("usage"), expected | {"output_tokens": 0})
        self.reply = self.codex_reply
        run = self.ok("Missing Codex usage", backend="codex")
        self.assertEqual(self.manifest(run).get("usage"), expected)
        self.reply = lambda req, argv: self.codex_reply(
            req, argv, stdout=b'{"type":"thread.started"}\n')
        run = self.ok("Codex message without usage event", backend="codex", audit=True)
        self.assertEqual(self.manifest(run).get("usage"), expected)

    def test_cout_sans_prompt(self):
        for label, reply, expected in (
            ("Blocked prompt", lambda req: answer(req).replace("Synthetic prompt.", "BLOCKED: Which format?"), 3),
            ("Missing markers", lambda req: "Plain text.", 2),
        ):
            with self.subTest(label=label):
                self.reply = lambda req, argv: self.json_reply(claude_result(req, result=reply(req)))
                code, error, run = self.call(label)
                self.assertEqual(code, expected, error)
                self.assertFalse((run / "prompt.md").exists())
                self.assertTrue((run / "manifest.json").exists())
                self.assertEqual(self.manifest(run)["usage"]["cost_usd"], 0.25)


class Reprise(BackendTest):
    def resume(self, call=-1):
        argv = self.calls[call][0]
        return argv[argv.index("--resume") + 1] if "--resume" in argv else None

    @property
    def state(self):
        return self.out / ".quick-session.json"

    @property
    def lock(self):
        return self.out / ".quick-session.lock"

    def test_regle(self):
        opts = ("--quick", "--model", "model-a", "--backend-arg=--effort=high")
        scope = self.ok("Seed session", *opts)
        self.assertFalse("--no-session-persistence" in self.calls[-1][0])
        self.assertIsNone(self.resume())
        original = self.state.read_bytes()
        self.ok("Normal is fresh", *opts[1:])
        self.assertIsNone(self.resume())
        self.assertIn("--no-session-persistence", self.calls[-1][0])
        self.ok("Audit is fresh", *opts[1:], audit=True)
        self.assertIsNone(self.resume())
        self.reply = self.codex_reply
        self.ok("Codex is fresh", "--quick", backend="codex")
        self.assertIsNone(self.resume())
        self.assertIn("--ephemeral", self.calls[-1][0])
        self.assertEqual(self.state.read_bytes(), original)
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="session-two"))
        self.now += 3599
        run = self.ok("Eligible quick", *opts)
        self.assertEqual(self.resume(), "session-one")
        self.assertEqual(self.manifest(run).get("session"),
                         {"reused": True, "age_s": 3599, "context_tokens": 124})
        self.assertEqual(self.manifest(scope).get("session"),
                         {"reused": False, "age_s": None, "context_tokens": 124})
        self.assertEqual(json.loads(self.state.read_text(encoding="utf-8"))["session_id"], "session-two")
        self.now += 1
        fresh = [
            ("expired", opts, {}, 3600),
            ("other model", ("--quick", "--model", "model-b", opts[-1]), {}, 1),
            ("other options", opts[:-1], {}, 1),
            ("other role hash", opts, {"role_sha256": "different"}, 1),
            ("other backend", opts, {"backend": "codex"}, 1),
            ("at context limit", opts, {"context_tokens": 150000}, 1),
            ("above context limit", opts, {"context_tokens": 190000}, 1),
        ]
        for label, args, changes, age in fresh:
            with self.subTest(label=label):
                state = json.loads(original) | changes | {"created": self.now - age}
                self.state.write_text(json.dumps(state), encoding="utf-8")
                self.ok(label, *args)
                self.assertIsNone(self.resume())
        for label, context in (("over bound with cache", (2, 187000, 4600)), ("unknown context", None)):
            with self.subTest(label=label):
                self.state.unlink(missing_ok=True)
                self.reply = lambda req, argv: self.json_reply(claude_result(req, context=context))
                self.ok(f"Seed {label}", *opts)
                self.ok(label, *opts)
                self.assertIsNone(self.resume())

    def test_cout_propre(self):
        for i, (total, tokens, expected_cost) in enumerate(
                ((0.25, 12, 0.25), (0.68, 23, 0.43), (0.75, 2, 0.07),
                 (None, 14, None), (0.92, 5, None)), start=1):
            with self.subTest(turn=i):
                self.reply = lambda req, argv: self.json_reply(claude_result(req, cost=total, tokens=tokens))
                run = self.ok(f"Quick usage {i}", "--quick")
                usage = self.manifest(run).get("usage", {})
                self.assertEqual(usage.get("cost_usd"), expected_cost)
                self.assertEqual(usage.get("output_tokens"), tokens)
                self.assertEqual(self.manifest(run).get("session", {}).get("reused"), i > 1)
            self.now += 5

    def test_parallele(self):
        self.ok("Seed parallel", "--quick")
        seed_state = self.state.read_bytes() if self.state.exists() else None
        count = len(self.calls)
        read_bytes = Path.read_bytes

        def read_without_state(path):
            self.assertNotEqual(path, self.state, "a contender must not read session state")
            return read_bytes(path)

        def overlapping(req, argv):
            if b"\nConcurrent failure\n" in req:
                return subprocess.CompletedProcess([], 1, b"", b"Failed independently")
            if b"\nLock holder\n" not in req:
                return self.json_reply(claude_result(req, session="independent"))
            with patch.object(Path, "read_bytes", read_without_state):
                self.ok("Concurrent quick", "--quick")
                code, error, _ = self.call("Concurrent failure", "--quick")
                self.assertEqual(code, 2, error)
                self.assertIsNone(self.resume())
            self.assertIsNone(self.resume(count + 1))
            self.assertTrue(self.lock.exists())
            self.assertEqual(self.state.read_bytes(), seed_state)
            return self.json_reply(claude_result(req, session="lock-holder"))

        self.reply = overlapping
        self.ok("Lock holder", "--quick")
        self.assertEqual(len(self.calls) - count, 3)
        self.assertEqual(self.resume(count), "session-one")
        self.assertEqual(json.loads(self.state.read_bytes())["session_id"], "lock-holder")
        self.assertFalse(self.lock.exists())

        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="after-stale"))
        self.lock.touch()
        os.utime(self.lock, (self.now - 3600,) * 2)
        self.ok("Lock at age limit", "--quick")
        self.assertIsNone(self.resume())
        self.assertTrue(self.lock.exists())
        self.now += 1
        self.ok("Stale lock ignored", "--quick")
        self.assertEqual(self.resume(), "lock-holder")
        self.assertFalse(self.lock.exists())
        self.assertEqual(json.loads(self.state.read_bytes())["session_id"], "after-stale")

    def test_parallele_proprietaire_expire(self):
        self.ok("Seed expired owner", "--quick")

        def overlapping(req, argv):
            if b"\nExpired owner\n" not in req:
                return self.json_reply(claude_result(req, session="new-owner"))
            self.now += 3601
            self.ok("New lock owner", "--quick")
            return self.json_reply(claude_result(req, session="expired-owner"))

        self.reply = overlapping
        self.ok("Expired owner", "--quick")
        self.assertEqual(json.loads(self.state.read_bytes())["session_id"], "new-owner")
        self.assertFalse(self.lock.exists())

    def test_echec(self):
        self.ok("Seed failed resume", "--quick")
        original = self.reply
        self.reply = lambda req, argv: subprocess.CompletedProcess([], 1, b"", b"Session not found")
        count = len(self.calls)
        code, error, run = self.call("Fail on resume", "--quick")
        self.assertEqual(code, 2)
        self.assertEqual(len(self.calls) - count, 1)
        self.assertEqual(self.resume(), "session-one")
        self.assertFalse(self.state.exists())
        self.assertFalse(self.lock.exists())
        self.assertIn("Session not found", error)
        self.assertIn("run again to start a fresh session", error)
        self.assertTrue((run / "response_raw.md").is_file())
        self.reply = original
        self.ok("Following quick is fresh", "--quick")
        self.assertIsNone(self.resume())


class Plug(BackendTest):
    def test_prefixe(self):
        del os.environ["PCE_PLUGS"]
        self.plugs.write_text('launch = ["launcher", "two words", "*"]\n', encoding="utf-8")
        run = self.ok("Prefixed generation")
        argv, kwargs = self.calls[-1]
        role = next(run.glob("role_*.md"))
        direct = pce.backend_command("claude", self.executables["claude"], role, None, [], Path("last.md"))
        self.assertEqual(argv, [self.executables["launcher"], "two words", "*", *direct])
        self.assertEqual(kwargs["input"], (run / "request.md").read_bytes())
        self.assertEqual(kwargs["cwd"], ROOT)
        self.assertFalse(kwargs.get("shell", False))
        self.assertEqual(self.manifest(run).get("launch_plug"), True)

        override = self.home / "override.toml"
        override.write_text(f'launch = [{json.dumps(self.executables["launcher"])}, "override"]\n',
                            encoding="utf-8")
        os.environ["PCE_PLUGS"] = str(override)
        run = self.ok("Prefixed audit", audit=True)
        self.assertEqual(self.calls[-1][0][:2], [self.executables["launcher"], "override"])
        self.assertEqual(self.manifest(run).get("launch_plug"), True)

        self.reply = lambda req, argv: subprocess.CompletedProcess([], 99, b"", b"Launch failed")
        count = len(self.calls)
        code, error, _ = self.call("Failing launch executable")
        self.assertEqual(code, 2, error)
        self.assertIn("Launch failed", error)
        self.assertEqual(len(self.calls) - count, 1)

    def test_absente(self):
        del os.environ["PCE_PLUGS"]
        for label, path in (("Default absent", None), ("Path disabled", ""), ("Override absent", "unused.toml")):
            with self.subTest(label=label):
                if path is not None:
                    self.plugs.write_text('launch = ["launcher"]\n', encoding="utf-8")
                    os.environ["PCE_PLUGS"] = path
                run = self.ok(label)
                role = next(run.glob("role_*.md"))
                direct = pce.backend_command("claude", self.executables["claude"], role, None, [], Path("last.md"))
                self.assertEqual(self.calls[-1][0], direct)
                self.assertIs(self.manifest(run).get("launch_plug"), False)

    def test_invalide(self):
        os.environ["PCE_PLUGS"] = str(self.plugs)
        variants = {
            "not a list": b'launch = "launcher"',
            "empty list": b'launch = []',
            "non-string arg": b'launch = ["launcher", 1]',
            "unknown key": b'launch = ["launcher"]\nextra = true',
            "invalid TOML": b'launch = [',
            "invalid UTF-8": b'launch = ["\xff"]',
            "null byte argument": b'launch = ["launcher", "\\u0000"]',
            "missing executable": b'launch = ["missing-launcher"]',
            "empty executable": b'launch = [""]',
        }
        for label, data in variants.items():
            with self.subTest(label=label):
                self.plugs.write_bytes(data)
                code, error, _ = self.call(label)
                self.assertEqual(code, 2, error)
                self.assertEqual(len(self.calls), 0)
        self.plugs.unlink()
        self.plugs.mkdir()
        code, error, _ = self.call("Unreadable config")
        self.assertEqual(code, 2, error)
        self.assertEqual(len(self.calls), 0)
        if os.name != "nt":
            self.plugs.rmdir()
            self.plugs.symlink_to(self.home / "missing.toml")
            code, error, _ = self.call("Broken config link")
            self.assertEqual(code, 2, error)
            self.assertEqual(len(self.calls), 0)


class Release(unittest.TestCase):
    def test_version(self):
        self.assertEqual(pce.VERSION, "1.8.0")
        self.assertIn("## 1.8.0", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIn("# Verifications v1.8.0", (ROOT / "VERIFICATIONS.md").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("PCE_PLUGS", readme)
        self.assertNotIn("no file reading", readme)
