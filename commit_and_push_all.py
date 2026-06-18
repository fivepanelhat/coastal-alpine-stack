import os
import subprocess

ROOT = r"C:\Users\Admin\.gemini\antigravity-ide\scratch\coastal-alpine-stack"
SUBMODULES = [
    "AquaGuard-Portal",
    "Blue-Moon-Portal",
    "SoilGuard-Portal",
    "Sovereign-Edge-Firmware",
    "Sting-Operation-AI",
    "coastal_alpine_core",
    "fivepanelhat",
    "weaver",
    "Weaver"
]

def git_sync(repo_path, commit_msg):
    if not os.path.isdir(repo_path):
        return
    if not os.path.isdir(os.path.join(repo_path, ".git")) and not os.path.isfile(os.path.join(repo_path, ".git")):
        return
        
    print(f"\n--- Syncing {os.path.basename(repo_path)} ---")
    try:
        # Check current branch
        branch_res = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        branch = branch_res.stdout.strip()
        print(f"Current branch: {branch}")
        
        # Git add all changes (including untracked setup.md, installation.md)
        subprocess.run(
            ["git", "add", "-A"],
            cwd=repo_path,
            check=True
        )
        
        # Check if there are staged changes to commit
        diff_res = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=repo_path
        )
        if diff_res.returncode == 0:
            print("No staged changes to commit.")
            return
            
        # Commit
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=repo_path,
            check=True
        )
        print("Committed successfully.")
        
        # Push
        subprocess.run(
            ["git", "push", "origin", branch],
            cwd=repo_path,
            check=True
        )
        print("Pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error in {os.path.basename(repo_path)}: {e}")

# Commit and push all submodules first
for sub in SUBMODULES:
    sub_path = os.path.join(ROOT, sub)
    git_sync(sub_path, "docs: separate Windows/Linux installation guides and fix CI/CD")

# Commit and push root monorepo
git_sync(ROOT, "docs: separate Windows/Linux installation guides and fix CI/CD")
