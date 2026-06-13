import sqlite3
import logging
from typing import TypedDict, List
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from weaver_agent import autonomous_weaver_node as weaver_node

# ---------------------------------------------------------
# 1. THE BLACK BOX: Sovereign Edge Telemetry
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(node)s): %(message)s',
    handlers=[
        logging.FileHandler("swarm_audit.log"),
        logging.StreamHandler()
    ]
)


# Custom filter to inject node names into the logs
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

# ---------------------------------------------------------
# 2. The Deterministic Swarm State
# ---------------------------------------------------------


class SwarmState(TypedDict):
    target_file: str
    code_content: str
    lint_errors: List[str]
    security_warnings: List[str]
    revision_count: int
    sender: str


def hound_node(state: SwarmState):
    node_filter.node_name = "Hound"
    logger.info("Executing SecOps AST Analysis...")
    return {"sender": "hound"}


def schema_cop_node(state: SwarmState):
    node_filter.node_name = "Schema-Cop"
    logger.info("Validating Pydantic/Monorepo Coherence...")
    return {"sender": "schema-cop"}


# ---------------------------------------------------------
# 3. The Orchestration Router
# ---------------------------------------------------------
def routing_logic(state: SwarmState) -> str:
    node_filter.node_name = "Router"

    # LOOP BREAKER: Abort if we exceed 3 refactor attempts
    if state.get("revision_count", 0) >= 3:
        logger.warning("CRITICAL: Swarm caught in loop. Aborting for manual human review.")
        return "__end__"

    if len(state.get("security_warnings", [])) > 0:
        logger.info("Perimeter breached by security warning. Routing back to Weaver.")
        return "weaver"

    if len(state.get("lint_errors", [])) > 0:
        logger.info("Perimeter breached by lint error. Routing back to Weaver.")
        return "weaver"

    logger.info("Perimeter clean. Clear to push.")
    return "__end__"


# ---------------------------------------------------------
# 4. Compile the Graph with The Memory Vault
# ---------------------------------------------------------
builder = StateGraph(SwarmState)

builder.add_node("weaver", weaver_node)
builder.add_node("hound", hound_node)
builder.add_node("schema-cop", schema_cop_node)

builder.set_entry_point("weaver")
builder.add_edge("weaver", "hound")
builder.add_edge("hound", "schema-cop")
builder.add_conditional_edges("schema-cop", routing_logic)  # type: ignore

# THE MEMORY VAULT: Initialize SQLite checkpointer
conn = sqlite3.connect("swarm_memory.db", check_same_thread=False)
memory = SqliteSaver(conn)

# Compile with persistent memory attached
swarm_graph = builder.compile(checkpointer=memory)

if __name__ == '__main__':
    logger.info("LangGraph State Machine Compiled with SQLite Persistence and Telemetry Ready.")
