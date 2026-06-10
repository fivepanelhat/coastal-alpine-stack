import os
import subprocess
import textwrap
import sys

WORKSPACE = r"C:\\Users\\Admin\\.gemini\\antigravity-ide\\scratch\\coastal-alpine-stack"

# Workflow definitions with an 8‑hour schedule (UTC midnight start)
SECOPS = textwrap.dedent('''
name: SecOps Scan
on:
  schedule:
    - cron: "0 */8 * * *"   # every 8 hours starting at 00:00 UTC
  push:
    branches: [ main ]
  pull_request:
    types: [ opened, synchronize, reopened ]
permissions:
  contents: read
  security-events: write
jobs:
  static-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run CodeQL analysis
        uses: github/codeql-action/init@v2
        with:
          languages: python
      - name: Perform CodeQL analysis
        uses: github/codeql-action/analyze@v2
''')

REDTEAM = textwrap.dedent('''
name: RedTeam Tests
on:
  schedule:
    - cron: "0 */8 * * *"
  workflow_dispatch:
permissions:
  contents: read
jobs:
  redteam:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install OWASP ZAP
        run: |
          sudo apt-get update && sudo apt-get install -y zaproxy
      - name: Run ZAP baseline scan
        run: |
          zap-baseline.py -t https://example.com -g gen -r zap_report.html
      - name: Upload ZAP report
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: zap_report.html
''')

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
''')

def write_workflow(repo_path, name, content):
    wf_dir = os.path.join(repo_path, '.github', 'workflows')
    os.makedirs(wf_dir, exist_ok=True)
    file_path = os.path.join(wf_dir, f"{name}.yml")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path

added = []
for repo in os.listdir(WORKSPACE):
    repo_path = os.path.join(WORKSPACE, repo)
    if not os.path.isdir(repo_path) or repo.startswith('.'):
        continue
    added.append(write_workflow(repo_path, 'secops', SECOPS))
    added.append(write_workflow(repo_path, 'redteam', REDTEAM))
    added.append(write_workflow(repo_path, 'ci-scan', CISCAN))
    # Stage changes
    try:
        subprocess.run(['git', 'add', '.github/workflows'], cwd=repo_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Check if there are staged changes
        diff = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=repo_path)
        if diff.returncode == 0:
            # No changes to commit
            continue
        # Commit with ASCII‑only message
        subprocess.run(['git', 'commit', '-m', 'Add/Update 8-hour scheduled CI, SecOps, RedTeam workflows'], cwd=repo_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Push to remote (assumes remote "origin" and branch "main")
        subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'], cwd=repo_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        # Print error using UTF‑8 to avoid encode issues
        sys.stderr.write(f"Git error in {repo}: {e}\n")

print('Scheduled workflows added/updated for repositories:')
for p in added:
    print(p)
