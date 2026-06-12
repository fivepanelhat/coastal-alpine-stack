import os
import subprocess

WORKSPACE = (
    r"C:\Users\Admin\.gemini\antigravity-ide\scratch\coastal-alpine-stack"
)

CI_SCAN = """
name: CI Scan
on:
  schedule:
    - cron: "0 */8 * * *"
  push:
    branches: [ master, main ]
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


def run(args, cwd):
    return subprocess.run(
        args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


# ── Sovereign-Edge-Firmware: push to master ────────────────────────────────
sov = os.path.join(WORKSPACE, "Sovereign-Edge-Firmware")
print("=== Sovereign-Edge-Firmware ===")

# Write ci-scan.yml
wf_dir = os.path.join(sov, ".github", "workflows")
os.makedirs(wf_dir, exist_ok=True)
with open(os.path.join(wf_dir, "ci-scan.yml"), "w", encoding="utf-8") as f:
    f.write(CI_SCAN)

# Write .nvmrc and .node-version
for vf in [".nvmrc", ".node-version"]:
    with open(os.path.join(sov, vf), "w", encoding="utf-8") as f:
        f.write("24\n")

# Stage
run(["git", "add", "-A"], cwd=sov)

# Check staged changes
diff = run(["git", "diff", "--cached", "--quiet"], cwd=sov)
if diff.returncode == 0:
    print("  no changes to commit after write — checking git status:")
    st = run(["git", "status", "--short"], cwd=sov)
    print(f"  {st.stdout.decode()}")
else:
    try:
        r = subprocess.run(
            [
                "git",
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-m",
                "Upgrade Node.js 20 to 24; ci-scan Node 24 step; add .nvmrc",
            ],
            cwd=sov,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"  committed: {r.stdout.decode().strip()}")
        push = subprocess.run(
            ["git", "push", "--set-upstream", "origin", "master"],
            cwd=sov,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("  pushed to master: OK")
    except subprocess.CalledProcessError as e:
        print(f"  error: {e.stderr.decode(errors='replace').strip()}")

# ── coastal_alpine_core: report remote status ──────────────────────────────
core = os.path.join(WORKSPACE, "coastal_alpine_core")
print("\n=== coastal_alpine_core ===")
remote = run(["git", "remote", "-v"], cwd=core)
print(f"  remotes:\n    {remote.stdout.decode().strip()}")
log = run(["git", "log", "--oneline", "-3"], cwd=core)
print(f"  last 3 commits:\n    {log.stdout.decode().strip()}")
print(
    "  ACTION NEEDED: Create the GitHub repo 'fivepanelhat/coastal_alpine_core'"
)
print("  then run: git push --set-upstream origin main")
print(
    "  (or push to the correct remote if it already exists under a different name)"
)
