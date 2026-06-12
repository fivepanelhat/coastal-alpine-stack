import os
import subprocess

WORKSPACE = (
    r"C:\Users\Admin\.gemini\antigravity-ide\scratch\coastal-alpine-stack"
)
core = os.path.join(WORKSPACE, "coastal_alpine_core")

TOKEN = os.environ.get("CI_PAT2", "")
if not TOKEN:
    print("ERROR: CI_PAT2 environment variable not set")
    raise SystemExit(1)

ORG = "coastal-alpine-stack"
REPO = "coastal_alpine_core"
REMOTE_URL = f"https://{ORG}:{TOKEN}@github.com/{ORG}/{REPO}.git"


def run(args, cwd, check=False):
    return subprocess.run(
        args,
        cwd=cwd,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


# Update remote to correct org
run(["git", "remote", "set-url", "origin", REMOTE_URL], cwd=core)
print("Remote URL updated to coastal-alpine-stack org (token not echoed)")

# Stage anything pending
run(["git", "add", "-A"], cwd=core)

# Commit if staged changes exist
diff = run(["git", "diff", "--cached", "--quiet"], cwd=core)
if diff.returncode != 0:
    try:
        subprocess.run(
            [
                "git",
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-m",
                "Upgrade Node.js 20 to 24; add ci-scan Node step",
            ],
            cwd=core,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Committed pending changes")
    except subprocess.CalledProcessError as e:
        print(f"Commit error: {e.stderr.decode(errors='replace').strip()}")
else:
    print("Nothing new to commit — pushing existing commits")

# Push
try:
    subprocess.run(
        ["git", "push", "--set-upstream", "origin", "main"],
        cwd=core,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print("coastal_alpine_core: pushed to main successfully")
except subprocess.CalledProcessError as e:
    err = e.stderr.decode(errors="replace").strip().replace(TOKEN, "***")
    print(f"Push error: {err}")
