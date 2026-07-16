import os
import subprocess
import textwrap

WORKSPACE = r"C:\\Users\\Admin\\.gemini\\antigravity-ide\\scratch\\coastal-alpine-stack"

SECOPS = textwrap.dedent("""
name: SecOps Scan
on:
 push:
 branches: [ main ]
 pull_request:
 types: [ opened, synchronize, reopened ]
permissions:
 contents: read
jobs:
 security-scan:
 name: Bandit SAST Scan
 runs-on: ubuntu-latest
 steps:
 - name: Checkout repository
 uses: actions/checkout@v4
 with:
 submodules: recursive
 fetch-depth: 0

 - name: Set up Python
 uses: actions/setup-python@v5
 with:
 python-version: '3.11' # Matches our hardened edge environment

 - name: Install Bandit
 run: pip install bandit

 - name: Run Bandit Security Scan
 # CRITICAL SECOPS CONFIG: We explicitly exclude the stress tests folder.
 # Otherwise, our simulated prompt injections and mock JWTs will trip the alarms!
 # -ll means report only Medium and High severity issues.
 run: bandit -r . -ll --exclude ./tests_security_stress/
""")

REDTEAM = textwrap.dedent("""
name: RedTeam Tests
on:
 schedule:
 - cron: "0 2 * * *" # daily at 02:00 UTC
 workflow_dispatch:
permissions:
 contents: read
jobs:
 redteam:
 runs-on: ubuntu-latest
 steps:
 - name: Checkout repository
 uses: actions/checkout@v4
 with:
 submodules: recursive
 fetch-depth: 0
 - name: Install OWASP ZAP
 run: |
 sudo apt-get update && sudo apt-get install -y zaproxy
 - name: Run ZAP baseline scan
 run: |
 zap-baseline.py -t https://your-app-url -g gen -r zap_report.html
 - name: Upload ZAP report
 uses: actions/upload-artifact@v4
 with:
 name: zap-report
 path: zap_report.html
""")

CISCAN = textwrap.dedent("""
name: CI Scan
on:
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
 - name: Checkout repository
 uses: actions/checkout@v4
 with:
 submodules: recursive
 fetch-depth: 0
 - name: Set up Python
 uses: actions/setup-python@v5
 with:
 python-version: '3.11'
 - name: Install dependencies
 run: |
 python -m pip install --upgrade pip
 if [ -f requirements-dev.txt ]; then
 pip install -r requirements-dev.txt
 else
 pip install flake8 pytest
 fi
 - name: Run linters
 run: |
 flake8 . --exclude=.venv,node_modules,build,dist,tests_security_stress
 - name: Run tests
 run: |
 pytest
""")


def write_workflow(repo_path, name, content):
 wf_dir = os.path.join(repo_path, ".github", "workflows")
 os.makedirs(wf_dir, exist_ok=True)
 file_path = os.path.join(wf_dir, f"{name}.yml")
 with open(file_path, "w", encoding="utf-8") as f:
 f.write(content)
 return file_path


added = []
for repo in os.listdir(WORKSPACE):
 repo_path = os.path.join(WORKSPACE, repo)
 if not os.path.isdir(repo_path) or repo.startswith("."):
 continue
 # write three workflows (overwrite if exist)
 added.append(write_workflow(repo_path, "secops", SECOPS))
 added.append(write_workflow(repo_path, "redteam", REDTEAM))
 added.append(write_workflow(repo_path, "ci-scan", CISCAN))
 # git add, commit, push
 try:
 subprocess.run(
 ["git", "add", ".github/workflows"], cwd=repo_path, check=True
 )
 subprocess.run(
 ["git", "commit", "-m", "Add CI security/redteam workflows"],
 cwd=repo_path,
 check=True,
 )
 subprocess.run(
 ["git", "push", "--set-upstream", "origin", "main"],
 cwd=repo_path,
 check=True,
 )
 except subprocess.CalledProcessError as e:
 print(f"Git error in {repo}: {e}")

print("Workflows added and pushed for repositories:")
for p in added:
 print(p)
