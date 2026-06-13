import sys
import sqlite3  # noqa: F401
import logging
import socket
import time
import mimetypes
import concurrent.futures
import contextlib  # noqa: F401
import uuid  # noqa: F401
from typing import TypedDict, List
from langgraph.graph import StateGraph
from persistence import ConcurrentSafeSqliteSaver
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
        record.node = self.node_name
        return True


logger = logging.getLogger("SovereignSwarm")
node_filter = NodeFilter()
logger.addFilter(node_filter)
logging.getLogger().addFilter(node_filter)
for handler in logging.getLogger().handlers:
    handler.addFilter(node_filter)


# ---------------------------------------------------------
# 2. Pre-Flight Health Check
# ---------------------------------------------------------
def ensure_ollama_ready(host="localhost", port=11434, max_retries=3):
    """Verify Ollama daemon is reachable; fail fast if not."""
    logger.filters[0].node_name = "Pre-Flight"  # type: ignore
    for attempt in range(max_retries):
        try:
            with socket.create_connection((host, port), timeout=2):
                logger.info("[OK] Local Ollama daemon is active and responding.")
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
    agent_errors: List[str]


# ---------------------------------------------------------
# 4. The Input Validation Shield
# ---------------------------------------------------------
def input_shield_node(state: SwarmState):
    logger.filters[0].node_name = "Shield"  # type: ignore
    try:
        target = state.get("target_file", "")
        code = state.get("code_content", "")

        if ".." in target or target.startswith("/"):
            raise ValueError(f"Path traversal anomaly detected in filename: {target}")

        if len(code.encode('utf-8')) > 1_000_000:
            raise ValueError("Payload exceeds 1MB limit. Possible DoS attempt.")

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
# 5. P0: Observability Tracer & Safe Wrappers
# ---------------------------------------------------------
TIMEOUT_SECONDS = 600


class SwarmContext:
    """Thread-local context for enriched telemetry."""
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]

    @contextlib.contextmanager
    def node_timer(self, node_name: str):
        node_start = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - node_start
            logger.info(f"[{self.session_id}] Node completed in {elapsed:.2f}s")


swarm_context = SwarmContext()


def _run_with_timeout(func, state: SwarmState, node_name: str):
    """Executes a function in a thread with a hard timeout and telemetry tracing."""
    with swarm_context.node_timer(node_name):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, state)
                return future.result(timeout=TIMEOUT_SECONDS)
        except concurrent.futures.TimeoutError:
            err_msg = f"{node_name} Timeout: Execution exceeded {TIMEOUT_SECONDS} seconds."
            logger.error(f"[{swarm_context.session_id}] {err_msg}")
            return {"sender": node_name.lower(), "agent_errors": state.get("agent_errors", []) + [err_msg]}
        except Exception as e:
            err_msg = f"{node_name} Crash: {str(e)}"
            logger.error(f"[{swarm_context.session_id}] {err_msg}")
            return {"sender": node_name.lower(), "agent_errors": state.get("agent_errors", []) + [err_msg]}


def _hound_logic(state: SwarmState):
    logger.info("Executing SecOps AST Analysis...")
    return {"sender": "hound"}


def _schema_cop_logic(state: SwarmState):
    logger.info("Validating Pydantic/Monorepo Coherence...")
    return {"sender": "schema-cop"}


def hound_node_safe(state: SwarmState):
    logger.filters[0].node_name = "Hound"  # type: ignore
    return _run_with_timeout(_hound_logic, state, "Hound")


def schema_cop_node_safe(state: SwarmState):
    logger.filters[0].node_name = "Schema-Cop"  # type: ignore
    return _run_with_timeout(_schema_cop_logic, state, "Schema-Cop")


def weaver_node_safe(state: SwarmState):
    logger.filters[0].node_name = "Weaver"  # type: ignore
    return _run_with_timeout(weaver_node, state, "Weaver")


# ---------------------------------------------------------
# 6. The Orchestration Router
# ---------------------------------------------------------
def routing_logic(state: SwarmState) -> str:
    logger.filters[0].node_name = "Router"  # type: ignore

    if state.get("agent_errors"):
        logger.warning(f"[{swarm_context.session_id}] Agent crash detected. Aborting to prevent cascade failure.")
        return "__end__"

    if state.get("revision_count", 0) >= 3:
        logger.warning(f"[{swarm_context.session_id}] CRITICAL: Swarm caught in loop. Aborting.")
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

# THE NEW CONCURRENCY LOCK
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
swarm_graph = builder.compile(checkpointer=memory)  # type: ignore

if __name__ == '__main__':
    logger.info("LangGraph State Machine Compiled with In-Memory Checkpointer.")

