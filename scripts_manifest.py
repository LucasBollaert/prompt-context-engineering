"""Write or check SHA256SUMS for the files this repository publishes.

The published files are those git would commit: tracked files plus untracked files that are not
ignored (`git ls-files --cached --others --exclude-standard`), minus SHA256SUMS itself. Ignored
paths such as out/, profils/local/ or .venv/ are therefore never listed. Run inside the git clone.

    python scripts_manifest.py           write SHA256SUMS
    python scripts_manifest.py --check   verify that SHA256SUMS lists exactly those files, with their hashes
"""
from pathlib import Path
import hashlib
import subprocess
import sys

root = Path(__file__).resolve().parent


def published() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                             cwd=root, capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        sys.exit(f"scripts_manifest.py must run inside the git clone ({e})")
    names = {n for n in out.decode("utf-8").split("\0") if n}
    return sorted(n for n in names if n != "SHA256SUMS" and (root / n).is_file())


def digest(name: str) -> str:
    return hashlib.sha256((root / name).read_bytes()).hexdigest()


if "--check" in sys.argv[1:]:
    listed = {}
    for line in (root / "SHA256SUMS").read_bytes().decode("utf-8").splitlines():
        h, name = line.split("  ", 1)
        listed[name] = h
    files = published()
    problems = [f"not listed: {n}" for n in files if n not in listed]
    problems += [f"listed but not published: {n}" for n in listed if n not in files]
    problems += [f"hash differs: {n}" for n in files if n in listed and listed[n] != digest(n)]
    print("\n".join(problems) or f"SHA256SUMS OK ({len(files)} files)")
    sys.exit(1 if problems else 0)

(root / "SHA256SUMS").write_bytes("".join(f"{digest(n)}  {n}\n" for n in published()).encode("utf-8"))
