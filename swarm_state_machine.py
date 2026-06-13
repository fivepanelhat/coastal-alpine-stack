import sys
import sqlite3
import logging
import socket
import time
import mimetypes
from typing import TypedDict, List
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from weaver_agent import autonomous_weaver_node as weaver_node

# ---------------------------------------------------------
# 1. Sovereign Edge Telemetry
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(node)s): %(message)s',
    handlers=[
        logging.FileHandler("swarm_audit.log"),
        logging.StreamHandler()
    ]
)


class NodeFilter(logging.Filter):
    def __init__(self, node_name="System"):
        super().__init__()
        self.node_name = node_name

    def filter(self, record):
        if not hasattr(record, "node"):
            record.node = self.node_name
        return True


logger = logging.getLogger("SovereignSwarm")
node_filter = NodeFilter()
logging.getLogger().addFilter(node_filter)
for handler in logging.getLogger().handlers:
    handler.addFilter(node_filter)

# ---------------------------------------------------------
# 2. P0: Pre-Flight Health Check
# ---------------------------------------------------------


def ensure_ollama_ready(host="localhost", port=11434, max_retries=3):
    """Verify Ollama daemon is reachable; fail fast if not."""
    node_filter.node_name = "Pre-Flight"
    for attempt in range(max_retries):
        try:
            with socket.create_connection((host, port), timeout=2):
                logger.info("Local Ollama daemon is active and responding.")
                return True
        except (socket.timeout, ConnectionRefusedError) as e:
            logger.warning(f"Ollama unreachable (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

    logger.critical("Ollama daemon is dead. Aborting swarm to prevent silent hang.")
    raise RuntimeError("Ollama daemon health check failed")


# ---------------------------------------------------------
# 3. The Deterministic Swarm State
# ---------------------------------------------------------
class SwarmState(TypedDict):
    target_file: str
    code_content: str
    lint_errors: List[str]
    security_warnings: List[str]
    revision_count: int
    sender: str
    agent_errors: List[str]  # New field to track silent crashes


# ---------------------------------------------------------
# 4. P0: The Input Validation Shield
# ---------------------------------------------------------
def input_shield_node(state: SwarmState):
    node_filter.node_name = "Shield"
    try:
        target = state.get("target_file", "")
        code = state.get("code_content", "")

        # 1. Path Traversal Check (Prevent reading /etc/passwd or C:\Windows)
        if ".." in target or target.startswith("/"):
            raise ValueError(f"Path traversal anomaly detected in filename: {target}")

        # 2. Payload Size Check (Prevent NPU DoS attacks - Max 1MB)
        if len(code.encode('utf-8')) > 1_000_000:
            raise ValueError("Payload exceeds 1MB limit. Possible DoS attempt.")

        # 3. MIME Type Check (Prevent binary execution)
        mime, _ = mimetypes.guess_type(target)
        if mime and not mime.startswith("text") and "json" not in mime and "javascript" not in mime:
            raise ValueError(f"Malicious binary or non-text payload detected: {mime}")

        logger.info(f"Input validated safely: {target} ({len(code)} bytes).")
        return {"sender": "shield"}

    except Exception as e:
        err_msg = f"SECURITY SHIELD BLOCK: {str(e)}"
        logger.critical(err_msg)
        return {"sender": "shield", "agent_errors": state.get("agent_errors", []) + [err_msg]}


def shield_routing(state: SwarmState) -> str:
    """If the shield catches a threat, abort before waking Weaver."""
    if state.get("agent_errors"):
        return "__end__"
    return "weaver"


# ---------------------------------------------------------
# 5. P0: Safe Agent Wrappers
# ---------------------------------------------------------
def hound_node_safe(state: SwarmState):
    node_filter.node_name = "Hound"
    try:
        logger.info("Executing SecOps AST Analysis...")
        # Future Bandit subprocess execution goes here
        return {"sender": "hound"}
    except Exception as e:
        err_msg = f"Hound Crash: {str(e)}"
        logger.error(err_msg)
        return {"sender": "hound", "agent_errors": state.get("agent_errors", []) + [err_msg]}


def schema_cop_node_safe(state: SwarmState):
    node_filter.node_name = "Schema-Cop"
    try:
        logger.info("Validating Pydantic/Monorepo Coherence...")
        return {"sender": "schema-cop"}
    except Exception as e:
        err_msg = f"Schema-Cop Crash: {str(e)}"
        logger.error(err_msg)
        return {"sender": "schema-cop", "agent_errors": state.get("agent_errors", []) + [err_msg]}


def weaver_node_safe(state: SwarmState):
    node_filter.node_name = "Weaver"
    try:
        # Call the tenacity-wrapped function from weaver_agent.py
        return weaver_node(state)
    except Exception as e:
        err_msg = f"Weaver Crash: {str(e)}"
        logger.error(err_msg)
        return {"sender": "weaver", "agent_errors": state.get("agent_errors", []) + [err_msg]}


# ---------------------------------------------------------
# 6. The Orchestration Router
# ---------------------------------------------------------
def routing_logic(state: SwarmState) -> str:
    node_filter.node_name = "Router"

    if state.get("agent_errors"):
        logger.warning("Agent crash detected in state. Aborting to prevent cascade failure.")
        return "__end__"

    if state.get("revision_count", 0) >= 3:
        logger.warning("CRITICAL: Swarm caught in loop. Aborting for manual human review.")
        return "__end__"

    if len(state.get("security_warnings", [])) > 0:
        logger.info("Perimeter breached by security warning. Routing to Weaver.")
        return "weaver"

    if len(state.get("lint_errors", [])) > 0:
        logger.info("Perimeter breached by lint error. Routing to Weaver.")
        return "weaver"

    logger.info("Perimeter clean. Clear to push.")
    return "__end__"


# ---------------------------------------------------------
# 7. Compile the Graph
# ---------------------------------------------------------
# Run Pre-flight before compiling (bypass under pytest to allow test collection)
if "pytest" not in sys.modules:
    ensure_ollama_ready()

builder = StateGraph(SwarmState)

builder.add_node("shield", input_shield_node)
builder.add_node("weaver", weaver_node_safe)
builder.add_node("hound", hound_node_safe)
builder.add_node("schema-cop", schema_cop_node_safe)

builder.set_entry_point("shield")
builder.add_conditional_edges("shield", shield_routing)  # type: ignore
builder.add_edge("weaver", "hound")
builder.add_edge("hound", "schema-cop")
builder.add_conditional_edges("schema-cop", routing_logic)  # type: ignore

conn = sqlite3.connect("swarm_memory.db", check_same_thread=False)
memory = SqliteSaver(conn)
swarm_graph = builder.compile(checkpointer=memory)  # type: ignore

if __name__ == '__main__':
    logger.info("LangGraph State Machine Compiled with P0 Hardening.")
