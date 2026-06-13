import os
import hmac
import hashlib
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
import logging

# Import your hardened swarm
from swarm_state_machine import swarm_graph, SwarmState  # noqa: F401

# Load secure environment variables
load_dotenv()
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

# Initialize FastAPI
app = FastAPI(title="Sovereign Edge Webhook Relay")
logger = logging.getLogger("SovereignSwarm")


def verify_github_signature(payload_body: bytes, signature_header: str | None) -> bool:
    """Mathematically verify the webhook originated from GitHub."""
    if not signature_header:
        return False

    hash_object = hmac.new(WEBHOOK_SECRET.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    return hmac.compare_digest(expected_signature, signature_header)


def execute_swarm_async(target_file: str, thread_id: str):
    """Run the LangGraph state machine in the background."""
    logger.info(f"Waking swarm for file: {target_file} (Thread: {thread_id})")

    # In a production scenario, you would checkout the branch and read the real file here.
    # For now, we mock the vulnerable code injection.
    initial_state = {
        "target_file": target_file,
        "code_content": "def login(u, p):\n    if p == 'admin123':\n        return True",
        "lint_errors": ["E225 missing whitespace around operator"],
        "security_warnings": ["B105:hardcoded_password_string"],
        "revision_count": 0,
        "sender": "system",
        "agent_errors": []
    }

    config = {"configurable": {"thread_id": thread_id}}

    try:
        # Execute the hardened graph
        for event in swarm_graph.stream(initial_state, config):  # type: ignore
            pass  # The graph's internal SqliteSaver and Logger handle the output
        logger.info(f"Swarm execution complete for thread {thread_id}")
    except Exception as e:
        logger.error(f"Catastrophic swarm failure in background thread: {str(e)}")


@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    """Ingress endpoint for GitHub PR events."""

    # 1. Cryptographic Verification
    signature = request.headers.get("x-hub-signature-256")
    body = await request.body()

    if not verify_github_signature(body, signature):
        logger.warning("Intrusion detected: Invalid webhook signature.")
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 2. Parse Payload
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Ignore pings or irrelevant events
    if "pull_request" not in payload and "commits" not in payload:
        return {"status": "ignored", "message": "Not a PR or Push event"}

    # 3. Dispatch to Swarm
    # We generate a unique ID for SQLite memory tracking
    session_id = f"webhook-{uuid.uuid4().hex[:8]}"

    # In reality, you'd extract the specific changed files from the payload here.
    # We will pass a dummy file name for the architecture test.
    target_file = "auth_routes.py"

    # Send the execution to the background so we return 202 to GitHub instantly
    background_tasks.add_task(execute_swarm_async, target_file, session_id)

    return {"status": "accepted", "session_id": session_id, "message": "Swarm dispatched"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Sovereign Edge Webhook Relay on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
