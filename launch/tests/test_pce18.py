"""Launcher 1.8 contracts. All CLI responses are synthetic."""
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
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
                                     PATH=str(self.bin), PCE_PLUGS="", CLAUDE_CONFIG_DIR=""))
        self.enterContext(patch.object(pce, "time", create=True))
        pce.time.time.side_effect = lambda: self.now
        self.enterContext(patch.object(pce, "git_commit", return_value=None))
        self.enterContext(patch.object(pce.subprocess, "run", side_effect=self.dispatch))

    def dispatch(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        return self.reply(kwargs["input"], argv)

    def json_reply(self, obj):
        return subprocess.CompletedProcess([], 0, json.dumps(obj).encode(), b"")

    def arguments(self, label, *options, backend="claude", audit=False):
        action = ["audit", "--prompt-file", str(self.prompt), "--role", "design"] if audit else ["generate"]
        return [*action, "--backend", backend, "--need", label, "--out", str(self.out), *options]

    def run_for(self, label):
        run, = (path.parent for path in self.out.glob("*/request.md")
                if f"\n{label}\n" in path.read_text(encoding="utf-8"))
        return run

    def call(self, label, *options, **kwargs):
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            code = pce.main(self.arguments(label, *options, **kwargs))
        return code, err.getvalue(), self.run_for(label)

    def resume(self, call=-1):
        argv = self.calls[call][0]
        return argv[argv.index("--resume") + 1] if "--resume" in argv else None

    def ok(self, label, *options, **kwargs):
        code, error, run = self.call(label, *options, **kwargs)
        self.assertEqual(code, 0, error)
        return run

    def manifest(self, run):
        return json.loads((run / "manifest.json").read_text(encoding="utf-8"))

    @property
    def pool(self):
        return self.out / ".pce-sessions"

    def state(self, session="session-one"):
        return self.pool / f"{session}.json"

    def lock(self, session="session-one"):
        return self.pool / f"{session}.lock"

    def seed(self, session, context=(4, 100, 20), cost=0.25):
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session=session, cost=cost, context=context))
        return self.ok(f"Seed {session}")

    def codex_reply(self, request, argv, *, usage=None, last=True, stdout=None):
        if last:
            path = Path(argv[argv.index("--output-last-message") + 1])
            path.write_text(answer(request), encoding="utf-8")
        if stdout is None:
            stdout = (json.dumps({"type": "thread.started"}) + "\n"
                      + json.dumps({"type": "turn.completed", "usage": usage}) + "\n").encode()
        return subprocess.CompletedProcess([], 0, stdout, b"")


class Quick(unittest.TestCase):
    def test_argv_de_generation_identique(self):
        for extra in ([], ["--effort", "high"], ["--effort=low"]):
            with self.subTest(extra=extra):
                args = ("claude", "claude", pce.ROLE_FILES["designer"], "model-a", extra, Path("last.md"))
                standard = pce.backend_command(*args)
                self.assertEqual(pce.backend_command(*args, quick=True), standard)
                self.assertEqual([arg for arg in standard if arg.split("=", 1)[0] == "--effort"], extra[:1])

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
                    self.assertNotIn("--effort", quick)
                    self.assertNotIn("--effort", normal)
                    self.assertEqual(quick[quick.index("--system-prompt-file") + 1], str(role))
                else:
                    self.assertEqual(quick, normal)
                    self.assertFalse(any(arg.startswith("model_reasoning_effort=") for arg in normal))
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
    def test_manifeste_apres_echec_facture(self):
        empty = dict.fromkeys(("input_tokens", "cache_read", "cache_write", "output_tokens", "cost_usd"))
        billed = {"input_tokens": 3, "cache_read": 100, "cache_write": 20, "output_tokens": 12, "cost_usd": 0.25}
        for audit in (False, True):
            for kind in ("exit status", "error flag", "error subtype", "unreadable"):
                with self.subTest(audit=audit, kind=kind):
                    def failure(request, argv):
                        if kind == "unreadable":
                            return subprocess.CompletedProcess([], 0, b"not JSON", b"")
                        obj = claude_result(request, is_error=kind == "error flag",
                                            subtype="error" if kind == "error subtype" else "success")
                        return subprocess.CompletedProcess([], int(kind == "exit status"),
                                                           json.dumps(obj).encode(), b"")

                    self.reply = failure
                    count = len(self.calls)
                    code, error, run = self.call(f"Failed {kind} audit {audit}", audit=audit)
                    self.assertEqual(code, 2, error)
                    self.assertTrue((run / "manifest.json").is_file(), "backend errors must write a manifest")
                    manifest = self.manifest(run)
                    self.assertEqual(manifest["status"], "backend error")
                    self.assertEqual(manifest["cli_invocations"], len(self.calls) - count)
                    self.assertEqual(manifest["cli_invocations"], 1)
                    self.assertEqual(manifest["usage"], empty if kind == "unreadable" else billed)
                    self.assertEqual("session" in manifest, not audit)
                    if not audit:
                        self.assertFalse(manifest["session"]["saved"])

    def test_manifeste_codex_apres_echec_facture(self):
        counters = {"input_tokens": 31, "cached_input_tokens": 9, "output_tokens": 7}
        event = json.dumps({"type": "turn.completed", "usage": counters}).encode() + b"\n"
        for audit in (False, True):
            for kind in ("exit status", "missing last message", "unreadable event"):
                with self.subTest(audit=audit, kind=kind):
                    def failure(request, argv):
                        stdout = b"not JSON\n" + event if kind == "unreadable event" else event
                        proc = self.codex_reply(request, argv, last=kind != "missing last message", stdout=stdout)
                        proc.returncode = int(kind == "exit status")
                        return proc

                    self.reply = failure
                    code, error, run = self.call(f"Codex {kind} audit {audit}", backend="codex", audit=audit)
                    self.assertEqual(code, 2, error)
                    manifest = self.manifest(run)
                    self.assertEqual(manifest["status"], "backend error")
                    self.assertEqual(manifest["cli_invocations"], 1)
                    self.assertNotIn("session", manifest)
                    self.assertEqual(manifest["usage"], {
                        "input_tokens": 22, "cache_read": 9, "cache_write": None, "output_tokens": 7, "cost_usd": None,
                    })

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
    def test_standard_alimente_la_reserve(self):
        started = self.now

        def complete_standard(request, argv):
            self.now += 10
            return self.json_reply(claude_result(request))

        self.reply = complete_standard
        standard = self.ok("Standard seed")
        self.assertIsNone(self.resume())
        self.reply = lambda req, argv: self.json_reply(claude_result(req))
        quick = self.ok("Quick uses the standard seed", "--quick")
        self.assertEqual(self.resume(), "session-one", "quick must be able to resume a standard session")
        state = json.loads(self.state().read_bytes())
        self.assertEqual(state["account"], str((self.home / ".claude").resolve()))
        self.assertEqual(state["created"], started)
        self.assertEqual(state["last_used"], self.now)
        self.assertNotIn("--no-session-persistence", self.calls[0][0])
        self.assertEqual(self.manifest(standard)["session"]["saved"], True)
        self.assertEqual(self.manifest(quick)["session"]["resumed_origin"], "standard")
        self.assertEqual(self.manifest(quick)["session"]["age_s"], 10)
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="session-two"))
        self.ok("Second standard stays fresh")
        self.assertIsNone(self.resume())

    def test_precision_isolement_et_requete_exacte(self):
        notice = getattr(pce, "RESUME_NOTICE", "Independent request.").encode("utf-8")
        fresh = self.ok("Fresh request", "--quick")
        fresh_stdin = self.calls[-1][1]["input"]
        self.assertFalse(fresh_stdin.startswith(notice))
        self.assertEqual((fresh / "request.md").read_bytes(), fresh_stdin)
        resumed = self.ok("Independent resumed request", "--quick")
        resumed_stdin = self.calls[-1][1]["input"]
        self.assertEqual(self.resume(), "session-one")
        self.assertTrue(resumed_stdin.startswith(notice + b"\n\n"), "resume must start with the isolation notice")
        self.assertEqual((resumed / "request.md").read_bytes(), resumed_stdin)
        nonce = re.search(rb"<<<PCE:([0-9a-f]+):BEGIN prompt>>>", resumed_stdin)[1].decode()
        expected = pce.build_generate_request(pce.builtin_profile(), "Independent resumed request", "", "", "", {},
                                              nonce, "English for instructions to the model; keep user-facing text "
                                              "and literal values in their original language", quick=True)
        self.assertEqual(resumed_stdin[len(notice) + 2:], expected.encode("utf-8"))
        self.assertFalse(self.manifest(fresh)["session"]["isolation_notice"])
        self.assertTrue(self.manifest(resumed)["session"]["isolation_notice"])

    def test_regle(self):
        opts = ("--quick", "--model", "model-a", "--backend-arg=--effort=high")
        scope = self.ok("Seed session", *opts)
        self.assertNotIn("--no-session-persistence", self.calls[-1][0])
        self.assertIsNone(self.resume())
        original = self.state().read_bytes()
        self.ok("Audit is fresh", *opts[1:], audit=True)
        self.assertIsNone(self.resume())
        self.assertIn("--no-session-persistence", self.calls[-1][0])
        self.reply = self.codex_reply
        self.ok("Codex is fresh", "--quick", backend="codex")
        self.assertIsNone(self.resume())
        self.assertIn("--ephemeral", self.calls[-1][0])
        self.assertEqual(list(self.pool.iterdir()), [self.state()])
        self.assertEqual(self.state().read_bytes(), original)
        self.reply = lambda req, argv: self.json_reply(claude_result(req))
        self.now += 3599
        run = self.ok("Eligible quick", *opts)
        self.assertEqual(self.resume(), "session-one")
        self.assertEqual(self.manifest(run).get("session"),
                         {"reused": True, "resumed_origin": "quick", "age_s": 3599, "context_tokens": 124,
                          "isolation_notice": True, "candidates": 1, "saved": True})
        self.assertEqual(self.manifest(scope).get("session"),
                         {"reused": False, "resumed_origin": None, "age_s": None, "context_tokens": 124,
                          "isolation_notice": False, "candidates": 0, "saved": True})
        state = json.loads(self.state().read_bytes())
        self.assertEqual(state, json.loads(original) | {"last_used": self.now})
        self.now += 1
        fresh = [
            ("expired", opts, {}, 3600),
            ("future", opts, {}, -1),
            ("other model", ("--quick", "--model", "model-b", opts[-1]), {}, 1),
            ("other options", opts[:-1], {}, 1),
            ("other role hash", opts, {"role_sha256": "different"}, 1),
            ("other backend", opts, {"backend": "codex"}, 1),
            ("at context limit", opts, {"context_tokens": 150000}, 1),
            ("above context limit", opts, {"context_tokens": 190000}, 1),
        ]
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="separate-session"))
        for label, args, changes, age in fresh:
            with self.subTest(label=label):
                state = json.loads(original) | changes | {"created": self.now - age}
                self.state().write_text(json.dumps(state), encoding="utf-8")
                self.ok(label, *args)
                self.assertIsNone(self.resume())
                self.state("separate-session").unlink()
        for label, context in (("over bound with cache", (2, 194840, 5058)), ("unknown context", None)):
            with self.subTest(label=label):
                self.state().unlink(missing_ok=True)
                self.reply = lambda req, argv: self.json_reply(claude_result(req, context=context))
                seeded = self.ok(f"Seed {label}", *opts)
                self.assertEqual(self.manifest(seeded)["session"]["context_tokens"], sum(context) if context else None)
                self.ok(label, *opts)
                self.assertIsNone(self.resume())

    def test_choix_contexte_puis_derniere_utilisation(self):
        self.seed("light-old", (1, 1, 0))
        self.now += 1
        self.seed("light-newer", (0, 1, 2))
        self.now += 1
        self.seed("heavy-recent", (17, 3, 0))
        self.now += 1
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="light-old", context=(3, 0, 0)))
        self.ok("Lightest outranks more recent sessions", "--quick")
        self.assertEqual(self.resume(), "light-old")
        self.now += 1
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="light-old", context=(30, 0, 0)))
        self.ok("Most recent of equal contexts", "--quick")
        self.assertEqual(self.resume(), "light-old")
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="light-newer"))
        self.ok("Updated context changes the next choice", "--quick")
        self.assertEqual(self.resume(), "light-newer")

    def test_relecture_apres_acquisition(self):
        self.seed("stale-choice", (1, 0, 0))
        self.seed("valid-choice", (2, 0, 0))
        claim = pce.SessionPool.claim

        def update_after_claim(pool, session_id):
            claimed = claim(pool, session_id)
            if claimed and session_id == "stale-choice":
                state = json.loads(self.state(session_id).read_bytes())
                self.state(session_id).write_text(json.dumps(state | {"context_tokens": 150000}), encoding="utf-8")
            return claimed

        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="valid-choice"))
        with patch.object(pce.SessionPool, "claim", update_after_claim):
            self.ok("Recheck context after taking the lock", "--quick")
        self.assertEqual(self.resume(), "valid-choice")
        self.assertEqual(list(self.pool.glob("*.lock")), [])

    def test_identifiants_invalides_et_entrees_illisibles(self):
        for index, session_id in enumerate(("--x", "../a", "x" * 129, "session\n")):
            with self.subTest(session_id=session_id):
                self.reply = lambda req, argv: self.json_reply(claude_result(req, session=session_id))
                run = self.ok(f"Unsafe id {index}", "--quick")
                self.assertIsNone(self.resume())
                self.assertFalse(self.manifest(run)["session"]["saved"])
                self.assertEqual(list(self.pool.glob("*")), [])
                self.assertFalse((self.out / "a.json").exists())
        self.seed("seed-for-corrupt-entries")
        original = self.state("seed-for-corrupt-entries")
        state = json.loads(original.read_bytes())
        original.unlink()
        for filename, session_id in (("valid-filename", "../a"), ("--x", "--x"), ("unexpected-name", "different")):
            self.state(filename).write_text(json.dumps(state | {"session_id": session_id}), encoding="utf-8")
        self.state("invalid-json").write_bytes(b"\xff")
        self.state("not-a-file").mkdir()
        self.state("invalid-time").write_text(json.dumps(state | {"session_id": "invalid-time", "created": -(10**400)}),
                                             encoding="utf-8")
        self.reply = lambda req, argv: self.json_reply(claude_result(req))
        self.ok("Ignore invalid entries", "--quick")
        self.assertIsNone(self.resume())

    def test_erreur_acces_reserve_avant_invocation(self):
        self.pool.write_bytes(b"not a directory")
        for options in ((), ("--quick",)):
            code, error, run = self.call(f"Inaccessible session pool {options}", *options)
            self.assertEqual(code, 2, error)
            self.assertIn("could not access Claude session pool", error)
            self.assertNotIn("Traceback", error)
            self.assertFalse((run / "manifest.json").exists())
        self.assertEqual(self.calls, [])

    def test_erreur_ecriture_reserve_apres_invocation(self):
        self.seed("session-one")
        for label, options, expected_resume in (("Failed update", ("--quick",), "session-one"),
                                                 ("Failed new entry", (), None)):
            with self.subTest(label=label):
                with patch.object(pce.os, "replace", side_effect=PermissionError("synthetic write failure")):
                    code, error, run = self.call(label, *options)
                self.assertEqual(code, 0, error)
                self.assertEqual(self.resume(), expected_resume)
                self.assertIn("warning", error)
                self.assertIn("synthetic write failure", error)
                self.assertNotIn("Traceback", error)
                self.assertTrue((run / "prompt.md").is_file())
                self.assertFalse(self.manifest(run)["session"]["saved"])
                self.assertEqual(list(self.pool.iterdir()), [])

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

    def test_cout_cumulatif_en_baisse(self):
        self.seed("session-one", cost=0.25)
        self.reply = lambda req, argv: self.json_reply(claude_result(req, cost=0.2, tokens=5))
        run = self.ok("Unknown incremental cost", "--quick")
        self.assertEqual(self.resume(), "session-one")
        self.assertIsNone(self.manifest(run)["usage"]["cost_usd"])
        self.assertEqual(self.manifest(run)["usage"]["output_tokens"], 5)
        self.assertEqual(json.loads(self.state().read_bytes())["total_cost_usd"], 0.2)

    def test_parallele(self):
        self.seed("light", (1, 0, 0))
        self.seed("heavy", (2, 0, 0))
        count = len(self.calls)
        first_entered = threading.Event()
        second_entered = threading.Event()
        release = threading.Event()

        def overlapping(req, argv):
            first = b"\nFirst concurrent quick\n" in req
            (first_entered if first else second_entered).set()
            self.assertTrue(release.wait(10), "test did not release the concurrent backends")
            return self.json_reply(claude_result(req, session="light" if first else "heavy"))

        self.reply = overlapping
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as err:
            with ThreadPoolExecutor(max_workers=2) as executor:
                first = executor.submit(pce.main, self.arguments("First concurrent quick", "--quick"))
                try:
                    self.assertTrue(first_entered.wait(5), "first generation never reached its backend")
                    second = executor.submit(pce.main, self.arguments("Second concurrent quick", "--quick"))
                    self.assertTrue(second_entered.wait(5), "second generation waited for the first lock")
                    self.assertEqual([self.resume(count), self.resume(count + 1)], ["light", "heavy"])
                    self.assertEqual(set(self.pool.glob("*.lock")), {self.lock("light"), self.lock("heavy")})
                finally:
                    release.set()
                self.assertEqual(first.result(timeout=5), 0, err.getvalue())
                self.assertEqual(second.result(timeout=5), 0, err.getvalue())
        self.assertEqual(len(self.calls) - count, 2)
        self.assertEqual(list(self.pool.glob("*.lock")), [])

    def test_verrou_ne_cede_pas_et_purge_sur_age_de_session(self):
        self.seed("old-session")
        self.lock("old-session").write_bytes(b"another-owner")
        os.utime(self.lock("old-session"), (self.now - 3601,) * 2)
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="new-session", context=None))
        self.ok("Existing lock cannot be broken", "--quick")
        self.assertIsNone(self.resume())
        self.assertEqual(self.lock("old-session").read_bytes(), b"another-owner")
        self.now += 7200
        self.ok("Retention boundary", "--quick")
        self.assertTrue(self.state("old-session").exists())
        self.assertTrue(self.lock("old-session").exists())
        self.now += 1
        self.ok("Expired entry and lock are collected", "--quick")
        self.assertFalse(self.state("old-session").exists())
        self.assertFalse(self.lock("old-session").exists())

    def test_parallele_proprietaire_expire(self):
        self.ok("Seed expired owner", "--quick")

        def overlapping(req, argv):
            if b"\nExpired owner\n" not in req:
                return self.json_reply(claude_result(req, session="new-owner"))
            self.now += 7201
            self.ok("New lock owner", "--quick")
            return self.json_reply(claude_result(req))

        self.reply = overlapping
        run = self.ok("Expired owner", "--quick")
        self.assertFalse(self.state().exists())
        self.assertEqual(json.loads(self.state("new-owner").read_bytes())["session_id"], "new-owner")
        self.assertFalse(self.manifest(run)["session"]["saved"])
        self.assertEqual(list(self.pool.glob("*.lock")), [])

    def test_echec(self):
        self.ok("Seed failed resume", "--quick")
        original = self.reply
        self.reply = lambda req, argv: subprocess.CompletedProcess([], 1, b"", b"Session not found")
        count = len(self.calls)
        code, error, run = self.call("Fail on resume", "--quick")
        self.assertEqual(code, 2)
        self.assertEqual(len(self.calls) - count, 1)
        self.assertEqual(self.resume(), "session-one")
        self.assertFalse(self.state().exists())
        self.assertFalse(self.lock().exists())
        self.assertIn("Session not found", error)
        self.assertTrue(error.rstrip().endswith("Run again: a fresh session will be used."))
        self.assertTrue((run / "response_raw.md").is_file())
        self.reply = original
        self.ok("Following quick is fresh", "--quick")
        self.assertIsNone(self.resume())


class Plug(BackendTest):
    def enable_plug(self):
        self.plugs.write_text('launch = ["launcher"]\n', encoding="utf-8")
        os.environ["PCE_PLUGS"] = str(self.plugs)

    def test_override_explicitement_absent(self):
        os.environ["PCE_PLUGS"] = str(self.home / "missing.toml")
        code, error, _ = self.call("Missing explicit override")
        self.assertEqual(code, 2, error)
        self.assertEqual(self.calls, [])

    def test_compte_direct_effectif(self):
        account_a = self.home / "configuration-a"
        account_a.mkdir()
        account_b = self.home / "configuration-b"
        account_b.mkdir()
        os.environ["CLAUDE_CONFIG_DIR"] = "~/configuration-a"
        self.ok("Seed other account", "--quick")
        os.environ["CLAUDE_CONFIG_DIR"] = str(account_b)
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="new-account-session"))
        run = self.ok("Quick under different configuration", "--quick")
        self.assertIsNone(self.resume())
        self.assertEqual(json.loads(self.state().read_bytes())["account"], str(account_a.resolve()))
        self.assertFalse(self.manifest(run)["session"]["reused"])
        env = self.calls[-1][1].get("env", {})
        self.assertNotIn("PCE_RESUME_CANDIDATES", env)
        self.assertNotIn("PCE_ACCOUNT_FILE", env)
        state = json.loads(self.state("new-account-session").read_bytes())
        self.assertEqual(state["account"], str(account_b.resolve()))

    def test_lanceur_garde_remplace_ou_retire_resume(self):
        account_a, account_b = (str((self.home / f"configuration-{name}").resolve()) for name in ("a", "b"))
        for action, used_id, account, total, expected_cost in (
                ("keep", "light-a", account_a, 0.68, 0.43),
                ("replace", "light-b", account_b, 0.68, 0.28),
                ("remove", "new-under-launcher", account_b, 0.68, 0.68)):
            with self.subTest(action=action):
                os.environ["PCE_PLUGS"] = ""
                self.out = self.home / f"runs-{action}"
                os.environ["CLAUDE_CONFIG_DIR"] = account_a
                self.seed("light-a", (5, 0, 0), cost=0.25)
                self.now += 1
                os.environ["CLAUDE_CONFIG_DIR"] = account_b
                self.seed("light-b", (1, 0, 0), cost=0.40)
                self.now += 1
                os.environ["CLAUDE_CONFIG_DIR"] = account_a
                self.seed("newest-heavy-a", (100, 0, 0), cost=0.50)
                before = {sid: self.state(sid).read_bytes() for sid in ("light-a", "light-b", "newest-heavy-a")}
                self.enable_plug()

                def launcher(request, argv):
                    env = self.calls[-1][1]["env"]
                    candidates = json.loads(env["PCE_RESUME_CANDIDATES"])
                    self.assertEqual(candidates, [{"account": account_a, "session_id": "light-a"},
                                                  {"account": account_b, "session_id": "light-b"}])
                    index = argv.index("--resume")
                    self.assertEqual(argv[index + 1], candidates[0]["session_id"])
                    self.assertEqual(set(self.pool.glob("*.lock")), {self.lock("light-a"), self.lock("light-b")})
                    effective = list(argv)
                    if action == "remove":
                        del effective[index:index + 2]
                    elif action == "replace":
                        effective[index + 1] = candidates[1]["session_id"]
                    returned_id = effective[index + 1] if "--resume" in effective else used_id
                    config = Path(env["PCE_ACCOUNT_FILE"])
                    self.assertTrue(config.parent.is_dir())
                    config.write_bytes(f"\n{account}\r\nignored\n".encode("utf-8"))
                    return self.json_reply(claude_result(request, session=returned_id, cost=total, tokens=6))

                self.reply = launcher
                self.now += 10
                run = self.ok(f"Launcher {action}", "--quick")
                manifest = self.manifest(run)
                self.assertEqual(manifest["session"], {
                    "reused": action != "remove", "resumed_origin": "standard" if action != "remove" else None,
                    "age_s": (12 if action == "keep" else 11) if action != "remove" else None,
                    "context_tokens": 124, "isolation_notice": True, "candidates": 2, "saved": True,
                })
                self.assertEqual(manifest["usage"]["cost_usd"], expected_cost)
                self.assertEqual(manifest["usage"]["output_tokens"], 6)
                entry = json.loads(self.state(used_id).read_bytes())
                self.assertEqual(entry["account"], account)
                self.assertEqual(entry["origin"], "quick" if action == "remove" else "standard")
                self.assertEqual(entry["created"], self.now if action == "remove" else json.loads(before[used_id])["created"])
                for sid in before.keys() - {used_id}:
                    self.assertEqual(self.state(sid).read_bytes(), before[sid])
                self.assertEqual(list(self.pool.glob("*.lock")), [])
                argv, kwargs = self.calls[-1]
                no_resume = pce.backend_command("claude", self.executables["claude"], next(run.glob("role_*.md")),
                                                None, [], Path("last.md"), launch=(self.executables["launcher"],))
                index = argv.index("--resume")
                self.assertEqual(argv[:index] + argv[index + 2:], no_resume)
                self.assertEqual(kwargs["input"], (run / "request.md").read_bytes())
                self.assertFalse(Path(kwargs["env"]["PCE_ACCOUNT_FILE"]).parent.exists())

    def test_lanceur_groupe_comptes_non_declares(self):
        self.enable_plug()

        def report_oversized_account(request, argv):
            env = self.calls[-1][1]["env"]
            self.assertEqual(json.loads(env["PCE_RESUME_CANDIDATES"]), [])
            Path(env["PCE_ACCOUNT_FILE"]).write_bytes(b"x" * 4097 + b"\n")
            return self.json_reply(claude_result(request, session="unknown-light", context=(1, 0, 0)))

        self.reply = report_oversized_account
        self.ok("Standard with oversized account tag")
        self.seed("unknown-heavy", (2, 0, 0))
        for sid in ("unknown-light", "unknown-heavy"):
            self.assertIsNone(json.loads(self.state(sid).read_bytes())["account"])
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="unknown-light"))
        self.ok("Quick with one unknown-account candidate", "--quick")
        self.assertEqual(self.resume(), "unknown-light")
        env = self.calls[-1][1]["env"]
        self.assertEqual(json.loads(env["PCE_RESUME_CANDIDATES"]), [{"account": None, "session_id": "unknown-light"}])

    def test_echec_lanceur_supprime_toutes_les_reservations(self):
        os.environ["CLAUDE_CONFIG_DIR"] = str(self.home / "a")
        self.seed("account-a", (1, 0, 0))
        self.seed("unreserved-a", (2, 0, 0))
        os.environ["CLAUDE_CONFIG_DIR"] = str(self.home / "b")
        self.seed("account-b", (3, 0, 0), cost=0.4)
        self.enable_plug()
        self.reply = lambda req, argv: self.json_reply(claude_result(req, session="account-b", cost=0.68, subtype="error"))
        count = len(self.calls)
        code, error, run = self.call("Unsuccessful launched resume", "--quick")
        self.assertEqual(code, 2, error)
        self.assertTrue(error.rstrip().endswith("Run again: a fresh session will be used."))
        self.assertEqual(len(self.calls) - count, 1)
        self.assertEqual(list(self.pool.iterdir()), [self.state("unreserved-a")])
        manifest = self.manifest(run)
        self.assertEqual(manifest["status"], "backend error")
        self.assertEqual(manifest["usage"]["cost_usd"], 0.28)
        self.assertEqual(manifest["session"]["candidates"], 2)
        self.assertFalse(manifest["session"]["saved"])

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
        for label, path in (("Default absent", None), ("Path disabled", "")):
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
