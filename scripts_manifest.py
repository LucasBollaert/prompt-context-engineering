from pathlib import Path
import hashlib
root = Path(__file__).resolve().parent
files = sorted(p for p in root.rglob('*') if p.is_file() and p.name != 'SHA256SUMS' and not any(x in {'.git', '__pycache__', '.venv', 'local', 'private'} for x in p.relative_to(root).parts))
(root / 'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n' for p in files), encoding='utf-8')
