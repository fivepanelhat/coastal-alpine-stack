import os
import re

roots = [
    r'C:\Users\Admin\.gemini\antigravity-ide\scratch\coastal-alpine-stack',
    r'C:\Users\Admin\GitNexus',
]
SKIP = {'.venv', '.git', 'node_modules', '__pycache__', '.pytest_cache'}
EXTS = {'.yml', '.yaml', '.json', '.toml', '.tf', '.env', '.nvmrc', '.node-version', ''}
PATTERNS = [
    re.compile(r'node[:\s\-]+20', re.I),
    re.compile(r'node:20', re.I),
    re.compile(r'nodejs.?20', re.I),
    re.compile(r'node-version.*20', re.I),
    re.compile(r'"node".*"20', re.I),
    re.compile(r'engines.*node.*20', re.I),
]

hits = []
for root in roots:
    if not os.path.isdir(root):
        continue
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for fname in files:
            _, ext = os.path.splitext(fname)
            if ext.lower() not in EXTS and fname not in {'Dockerfile', '.nvmrc', '.node-version'}:
                continue
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        if any(p.search(line) for p in PATTERNS):
                            hits.append((fpath, i, line.rstrip()))
            except Exception:
                pass

for fpath, i, line in hits:
    print(f"{fpath}:{i}: {line}")

print(f"\nTotal matches: {len(hits)} across {len(set(h[0] for h in hits))} files")
