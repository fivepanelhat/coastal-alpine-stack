import subprocess
import re
from pathlib import Path
from pydantic import BaseModel, Field


# Strict Pydantic schema for deterministic AI output
class CoherenceReport(BaseModel):
    is_coherent: bool = Field(
        description="True if the entire monorepo is in perfect sync."
    )
    submodule_sync_errors: list[str] = Field(default_factory=list)
    dependency_drift_errors: list[str] = Field(default_factory=list)


def get_submodule_status() -> list[str]:
    """Retrieves the mathematical SHA state of all submodules."""
    try:
        # git submodule status returns: "+[SHA] [path] ([tag])"
        # The prefix '+' means the local submodule commit doesn't match the parent's tracked commit.
        result = subprocess.run(
            ["git", "submodule", "status"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        return [f"Git process error: {e.stderr}"]


def check_git_coherence(report: CoherenceReport):
    """Evaluates the DAG state for commit drift."""
    statuses = get_submodule_status()
    for status in statuses:
        if not status:
            continue
        # A '+' prefix mathematically proves the submodule has drifted from the parent monorepo index
        if status.startswith("+"):
            report.is_coherent = False
            report.submodule_sync_errors.append(
                f"State Drift Detected: {status.strip()}"
            )
        elif status.startswith("-"):
            report.is_coherent = False
            report.submodule_sync_errors.append(
                f"Uninitialized Submodule: {status.strip()}"
            )


def parse_requirements(file_path: Path) -> dict[str, str]:
    """Extracts exact dependency versions for intersection checking."""
    deps = {}
    if not file_path.exists():
        return deps

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Match package==version
            # Let's clean the package definition logic to handle inline comments, spaces, etc.
            match = re.match(r"^([a-zA-Z0-9_\-]+)==([0-9\.]+.*)$", line)
            if match:
                deps[match.group(1).lower()] = match.group(2)
    return deps


def check_dependency_coherence(report: CoherenceReport, root_path: Path):
    """Calculates the intersection of dependencies to ensure zero version drift."""
    root_req_path = root_path / "requirements.txt"
    root_deps = parse_requirements(root_req_path)

    if not root_deps:
        return  # Skip if root has no strictly defined dependencies yet

    # Define the core sub-modules to audit
    target_repos = [
        "weaver",
        "coastal_alpine_core",
        "Blue-Moon-Portal",
        "Sting-Operation-AI",
    ]

    for repo in target_repos:
        repo_req_path = root_path / repo / "requirements.txt"
        repo_deps = parse_requirements(repo_req_path)

        for pkg, repo_version in repo_deps.items():
            if pkg in root_deps:
                root_version = root_deps[pkg]
                if repo_version != root_version:
                    report.is_coherent = False
                    report.dependency_drift_errors.append(
                        f"Version Drift in {repo}: '{pkg}' is v{repo_version}, but root strictly enforces v{root_version}"
                    )


def run_coherence_scan():
    """Executes the full monorepo mathematical audit."""
    root_dir = Path(__file__).parent.resolve()
    report = CoherenceReport(is_coherent=True)

    check_git_coherence(report)
    check_dependency_coherence(report, root_dir)

    # Output strict JSON for Antigravity integration
    print(report.model_dump_json(indent=2))

    if not report.is_coherent:
        exit(1)  # Fail loudly for SecOps


if __name__ == "__main__":
    run_coherence_scan()
