import os
import subprocess
import sys

WORKSPACE = r"C:\Users\Admin\.gemini\antigravity-ide\scratch\coastal-alpine-stack"
SKIP = {'.git', '__pycache__', 'node_modules', '.venv', '.pytest_cache'}


def git_op(repo_path, msg):
    try:
        r = subprocess.run(
            ['git', 'add', '-A'], cwd=repo_path,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        diff = subprocess.run(
            ['git', 'diff', '--cached', '--quiet'], cwd=repo_path
        )
        if diff.returncode == 0:
            return 'no-changes'
        subprocess.run(
            ['git', 'commit', '-m', msg], cwd=repo_path, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        subprocess.run(
            ['git', 'push', '--set-upstream', 'origin', 'main'],
            cwd=repo_path, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return 'pushed'
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode('utf-8', errors='replace') if e.stderr else ''
        return f'error: {stderr.strip()}'


# Retry coastal_alpine_core specifically
repos_to_retry = ['coastal_alpine_core']
for repo in repos_to_retry:
    repo_path = os.path.join(WORKSPACE, repo)
    if os.path.isdir(os.path.join(repo_path, '.git')):
        # Check git status
        status = subprocess.run(
            ['git', 'status', '--short'], cwd=repo_path,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"{repo} status:\n{status.stdout.decode()}")
        result = git_op(repo_path, 'Upgrade Node.js from 20 to 24 across all configs')
        print(f"{repo}: {result}")
    else:
        print(f"{repo}: not a git repo, skipping")

# Also push the updated ci-scan.yml (with Node 24) to all repos
print("\nPushing updated ci-scan.yml (Node 24) to all repos...")
CI_SCAN = """
name: CI Scan
on:
  schedule:
    - cron: "0 */8 * * *"
  push:
    branches: [ main ]
  pull_request:
    types: [ opened, synchronize, reopened ]
permissions:
  contents: read
  packages: read
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '24'
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Run linters
        run: flake8 .
      - name: Run tests
        run: pytest
"""

for repo in os.listdir(WORKSPACE):
    repo_path = os.path.join(WORKSPACE, repo)
    if not os.path.isdir(repo_path) or repo.startswith('.') or repo in SKIP:
        continue
    wf_dir = os.path.join(repo_path, '.github', 'workflows')
    ci_scan_path = os.path.join(wf_dir, 'ci-scan.yml')
    if not os.path.isdir(wf_dir):
        continue
    with open(ci_scan_path, 'w', encoding='utf-8') as f:
        f.write(CI_SCAN)
    result = git_op(repo_path, 'ci-scan: add Node.js 24 setup step')
    print(f"  {repo}: {result}")
