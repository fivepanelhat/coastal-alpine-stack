import os
import hmac
import hashlib
import uuid
import subprocess
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
import logging

# Import your hardened swarm
from swarm_state_machine import swarm_graph

# Load secure environment variables
load_dotenv()
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
GITHUB_PAT = os.getenv("GITHUB_PAT", "")
GITHUB_USER = os.getenv("GITHUB_USERNAME", "Sovereign-Swarm")

# Initialize FastAPI
app = FastAPI(title="Sovereign Edge Webhook Relay")
logger = logging.getLogger("SovereignSwarm")

# We mounted the repository to /app/repo in docker-compose
REPO_DIR = "/app/repo" 

def verify_github_signature(payload_body: bytes, signature_header: str | None) -> bool:
    # Diamond: fail closed. Without a configured secret we cannot authenticate
    # the sender — never validate against an empty HMAC key (forgeable).
    if not WEBHOOK_SECRET:
        logger.error("GITHUB_WEBHOOK_SECRET is not set; rejecting webhook (fail-closed).")
        return False
    if not signature_header:
        return False
    hash_object = hmac.new(WEBHOOK_SECRET.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)

def run_git(args: list) -> str:
    """Execute Git commands securely within the mounted repo directory."""
    result = subprocess.run(args, cwd=REPO_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Git command failed: {' '.join(args)}\n{result.stderr}")
        raise RuntimeError(f"Git error: {result.stderr}")
    return result.stdout.strip()

def execute_swarm_async(branch_name: str, target_file: str, thread_id: str):
    """The Autonomous GitOps Loop."""
    logger.info(f"Initiating Autonomous Loop for {target_file} on branch {branch_name}...")
    
    try:
        # 1. Sync the Local Repository with authenticated origin URL
        repo_url = f"https://{GITHUB_USER}:{GITHUB_PAT}@github.com/fivepanelhat/coastal-alpine-stack.git"
        run_git(["git", "remote", "set-url", "origin", repo_url])
        run_git(["git", "fetch", "origin"])
        run_git(["git", "checkout", branch_name])
        run_git(["git", "pull", "origin", branch_name])
        
        # 2. Read the Real File
        file_path = os.path.join(REPO_DIR, target_file)
        if not os.path.exists(file_path):
            logger.error(f"File {target_file} not found. Aborting.")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            real_code = f.read()

        # 3. Ignite the Swarm
        initial_state = {
            "target_file": target_file,
            "code_content": real_code,
            "lint_errors": ["Automated PR Check Triggered"], # In a full build, Flake8 output goes here
            "security_warnings": ["Automated SecOps Scan Triggered"], # Bandit output goes here
            "revision_count": 0,
            "sender": "system",
            "agent_errors": []
        }
        
        config = {"configurable": {"thread_id": thread_id}}
        final_state = None
        
        for event in swarm_graph.stream(initial_state, config):
            for node_name, state_update in event.items():
                final_state = state_update

        # 4. Write the Fixed Code to Disk
        if final_state and "code_content" in final_state:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_state["code_content"])
            logger.info(f"Fixed code written to {target_file}.")
            
            # 5. The Autonomous Push
            repo_url = f"https://{GITHUB_USER}:{GITHUB_PAT}@github.com/fivepanelhat/coastal-alpine-stack.git"
            run_git(["git", "config", "user.email", "swarm@sovereign-edge.local"])
            run_git(["git", "config", "user.name", "Sovereign Swarm AI"])
            run_git(["git", "add", target_file])
            
            # Check if there are actual changes to commit
            status = run_git(["git", "status", "--porcelain"])
            if status:
                run_git(["git", "commit", "-m", f"secops(swarm): autonomous remediation of {target_file}"])
                run_git(["git", "push", repo_url, branch_name])
                logger.info(f"✓ Mission Complete: Fixes pushed to GitHub branch '{branch_name}'.")
            else:
                logger.info("Swarm found no actionable vulnerabilities to commit.")
                
    except Exception as e:
        logger.error(f"Catastrophic failure in autonomous loop: {str(e)}")

@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    signature = request.headers.get("x-hub-signature-256")
    body = await request.body()
    
    if not verify_github_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    
    # Only react to Pull Requests being opened or updated
    if "pull_request" not in payload:
        return {"status": "ignored", "message": "Not a PR event"}
        
    action = payload.get("action")
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored", "message": f"Ignoring PR action: {action}"}

    # Extract the PR branch
    branch_name = payload["pull_request"]["head"]["ref"]
    session_id = f"pr-{payload['pull_request']['number']}-{uuid.uuid4().hex[:4]}"
    
    # For phase 1 of the real deployment, we will hardcode the target file 
    # we want the swarm to look at when a PR opens, to keep the test controlled.
    # (Phase 2 would parse `git diff` to find all changed files dynamically).
    target_file = "trigger.txt" 
    
    background_tasks.add_task(execute_swarm_async, branch_name, target_file, session_id)
    return {"status": "accepted", "session_id": session_id, "message": "Autonomous GitOps Dispatched"}
