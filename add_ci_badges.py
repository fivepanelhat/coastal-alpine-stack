import os
import re

WORKSPACE = r"C:\\Users\\Admin\\.gemini\\antigravity-ide\\scratch\\coastal-alpine-stack"
WORKFLOW = "secops.yml"
BRANCH = "main"
BADGE_TEMPLATE = "![CI](https://github.com/{owner}/{repo}/actions/workflows/{workflow}/badge.svg?branch={branch})"


def get_owner_repo(repo_path):
    # Try to read remote origin from git config
    config_path = os.path.join(repo_path, ".git", "config")
    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as cfg:
            for line in cfg:
                m = re.search(
                    r"url = https://github.com/([^/]+)/([^/]+)(?:\\.git)?",
                    line,
                )
                if m:
                    return m.group(1), m.group(2)
    # Fallback: use folder name as repo name and unknown owner
    repo_name = os.path.basename(repo_path)
    return "UNKNOWN_OWNER", repo_name


def has_badge(content):
    pattern = re.compile(
        r"!\\[CI\\].*github\\.com/.*/actions/workflows/"
        + re.escape(WORKFLOW)
        + r"/badge\\.svg\\?branch="
        + re.escape(BRANCH)
    )
    return bool(pattern.search(content))


added_files = []
for entry in os.listdir(WORKSPACE):
    repo_path = os.path.join(WORKSPACE, entry)
    if not os.path.isdir(repo_path) or entry.startswith("."):
        continue
    owner, repo = get_owner_repo(repo_path)
    badge_md = BADGE_TEMPLATE.format(
        owner=owner, repo=repo, workflow=WORKFLOW, branch=BRANCH
    )
    readme_path = None
    for fname in os.listdir(repo_path):
        if fname.lower().startswith("readme") and fname.lower().endswith(
            ".md"
        ):
            readme_path = os.path.join(repo_path, fname)
            break
    if readme_path and os.path.isfile(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        if has_badge(content):
            continue
        lines = content.splitlines()
        new_lines = []
        inserted = False
        for line in lines:
            new_lines.append(line)
            if not inserted and line.startswith("#"):
                new_lines.append("")
                new_lines.append(badge_md)
                new_lines.append("")
                inserted = True
        if not inserted:
            new_lines = [badge_md, ""] + lines
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
        added_files.append(readme_path)
    else:
        # Create a minimal README with title and badge
        readme_path = os.path.join(repo_path, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {repo}\n\n{badge_md}\n")
        added_files.append(readme_path)

print("CI badge added/updated in the following files:")
for p in added_files:
    print(p)
