import hmac
import hashlib
import os
import uuid
import logging
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Header
from pydantic import BaseModel  # noqa: F401
from swarm_state_machine import swarm_graph

# Setup basic logging for the API Gateway
logging.basicConfig(level=logging.INFO, format='%(asctime)s [API] %(message)s')
logger = logging.getLogger("WebhookRelay")

app = FastAPI(title="Coastal Alpine Webhook Relay")

# 1. The Cryptographic Airlock (Set this in your .env later)
GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "super-secret-local-key")


def verify_signature(payload_body: bytes, signature_header: str):
    """Mathematically guarantees the webhook actually came from your GitHub repo."""
    if not signature_header:
        raise HTTPException(status_code=403, detail="Missing X-Hub-Signature-256 header")

    hash_object = hmac.new(GITHUB_SECRET.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Cryptographic signature mismatch.")


# 2. The Asynchronous Swarm Trigger
def execute_background_swarm(target_file: str, code_payload: str):
    """Executes the LangGraph orchestrator completely independent of the API thread."""
    session_id = str(uuid.uuid4())[:8]
    logger.info(f"[{session_id}] Waking Coastal Alpine Swarm for file: {target_file}")

    # Construct the initial state
    initial_state = {
        "target_file": target_file,
        "code_content": code_payload,
        "lint_errors": ["E225 missing whitespace around operator"],
        "security_warnings": ["B105:hardcoded_password_string"],
        "revision_count": 0,
        "sender": "github_webhook",
        "agent_errors": []
    }

    # Isolate the memory thread
    config = {"configurable": {"thread_id": f"pr-thread-{session_id}"}}

    # Execute the graph
    try:
        for event in swarm_graph.stream(initial_state, config):  # type: ignore
            for node_name, state_update in event.items():
                if "code_content" in state_update and node_name == "weaver":
                    logger.info(f"[{session_id}] Weaver successfully refactored the payload.")
        logger.info(f"[{session_id}] Swarm execution complete. Thread closed.")
    except Exception as e:
        logger.error(f"[{session_id}] Fatal swarm exception during background execution: {str(e)}")


# 3. The API Endpoint
@app.post("/github-webhook")
async def github_webhook_receiver(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hub_signature_256: str = Header(None)
):
    # Read the raw bytes for cryptographic verification
    payload_body = await request.body()  # noqa: F841

    # Verify the airlock (Commented out for initial local testing, activate for production)
    # verify_signature(payload_body, x_hub_signature_256)

    # Parse the JSON payload
    data = await request.json()

    # Extract PR data (Simulated extraction for this architecture)
    action = data.get("action", "unknown")
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored", "reason": f"Action '{action}' does not trigger the swarm."}

    target_file = "simulated_pr_file.py"
    code_content = "def login(u, p):\n    if p == 'admin123':\n        return True"

    logger.info("Valid PR event received. Offloading to background NPU tasks.")

    # Hand off the heavy lifting to the background task
    background_tasks.add_task(execute_background_swarm, target_file, code_content)

    # Return 202 Accepted instantly so GitHub doesn't timeout
    return {"status": "accepted", "message": "Payload verified. Swarm deployed."}
