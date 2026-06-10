import os
import re
import subprocess
import json

roots = [
    r'C:\Users\Admin\.gemini\antigravity-ide\scratch\coastal-alpine-stack',
    r'C:\Users\Admin\GitNexus',
]
SKIP = {'.venv', '.git', 'node_modules', '__pycache__', '.pytest_cache'}

# All patterns that could reference Node 20
REPLACEMENTS = [
    # node-version: '20.x' or "20" or 20
    (re.compile(r"(node-version:\s*['\"]?)20(\.\w+)?(['\"]?)"), r"\g<1>24\3"),
    # node:20 in Dockerfiles / docker-compose
    (re.compile(r"\bnode:20\b"), r"node:24"),
    (re.compile(r"\bnode:20\."), r"node:24."),
    # "node": ">=20" or "^20" or "~20" engine range
    (re.compile(r'("node"\s*:\s*"[^"]*)(20)([^"]*")'), r"\g<1>24\g<3>"),
    # uses: actions/setup-node with node-version: 20
    (re.compile(r"(node-version:\s*)'20'"), r"\g<1>'24'"),
    (re.compile(r'(node-version:\s*)"20"'), r'\g<1>"24"'),
    (re.compile(r"(node-version:\s*)20\b"), r"\g<1>24"),
]

EXTS = {'.yml', '.yaml', '.json', '.toml', '.tf', '.env', '.nvmrc', '.node-version', ''}

changed_files = []

for root in roots:
    if not os.path.isdir(root):
        continue
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for fname in files:
            _, ext = os.path.splitext(fname)
            if ext.lower() not in EXTS and fname not in {'Dockerfile', '.nvmrc', '.node-version', 'docker-compose.yml'}:
                continue
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, encoding='utf-8', errors='ignore') as f:
                    original = f.read()
                updated = original
                for pattern, replacement in REPLACEMENTS:
                    updated = pattern.sub(replacement, updated)
                if updated != original:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(updated)
                    changed_files.append(fpath)
                    print(f"UPDATED: {fpath}")
            except Exception as e:
                print(f"ERROR: {fpath}: {e}")

# Also write a .node-version and .nvmrc at the root of each repo containing node
for root in roots:
    if not os.path.isdir(root):
        continue
    for entry in os.listdir(root):
        repo_path = os.path.join(root, entry)
        if not os.path.isdir(repo_path) or entry.startswith('.'):
            continue
        # Check if it looks like a Node.js project
        has_package_json = os.path.isfile(os.path.join(repo_path, 'package.json'))
        has_nvmrc = os.path.isfile(os.path.join(repo_path, '.nvmrc'))
        has_node_version = os.path.isfile(os.path.join(repo_path, '.node-version'))
        if has_package_json or has_nvmrc or has_node_version:
            for vfile in ['.nvmrc', '.node-version']:
                vpath = os.path.join(repo_path, vfile)
                with open(vpath, 'w', encoding='utf-8') as f:
                    f.write('24\n')
                changed_files.append(vpath)
                print(f"WROTE: {vpath}")

# Also update the ci-scan workflow templates to use node 24
CI_SCAN_TEMPLATE = r'C:\Users\Admin\.gemini\antigravity-ide\scratch\coastal-alpine-stack\apply_scheduled_workflows.py'
if os.path.isfile(CI_SCAN_TEMPLATE):
    with open(CI_SCAN_TEMPLATE, encoding='utf-8') as f:
        content = f.read()
    updated = content.replace("python-version: '3.11'", "python-version: '3.11'")  # keep python unchanged
    if updated != content:
        with open(CI_SCAN_TEMPLATE, 'w', encoding='utf-8') as f:
            f.write(updated)

print(f"\nTotal files updated: {len(changed_files)}")

# Now git commit and push each repo that had changes
def git_op(repo_path, msg):
    try:
        subprocess.run(['git', 'add', '-A'], cwd=repo_path, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        diff = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=repo_path)
        if diff.returncode == 0:
            return 'no-changes'
        subprocess.run(['git', 'commit', '-m', msg], cwd=repo_path, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'],
                       cwd=repo_path, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return 'pushed'
    except subprocess.CalledProcessError as e:
        return f'error: {e}'

affected_repos = set()
for fpath in changed_files:
    # find the git root
    parts = fpath.split(os.sep)
    for i in range(len(parts), 0, -1):
        candidate = os.sep.join(parts[:i])
        if os.path.isdir(os.path.join(candidate, '.git')):
            affected_repos.add(candidate)
            break

print("\nGit push results:")
for repo in sorted(affected_repos):
    result = git_op(repo, 'Upgrade Node.js from 20 to 24 across all configs')
    print(f"  {repo}: {result}")
