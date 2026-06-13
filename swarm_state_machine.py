from typing import TypedDict, List
from langgraph.graph import StateGraph


# 1. The Deterministic Swarm State
class SwarmState(TypedDict):
    target_file: str
    code_content: str
    lint_errors: List[str]
    security_warnings: List[str]
    revision_count: int
    sender: str  # Tracks which agent has the ball


# 2. Node Skeletons (The Agents)
from weaver_agent import autonomous_weaver_node as weaver_node  # noqa: E402


def hound_node(state: SwarmState):
    print("[Hound] Executing SecOps AST Analysis...")
    # Bandit API execution goes here
    return {"sender": "hound"}


def schema_cop_node(state: SwarmState):
    print("[Schema-Cop] Validating Pydantic/Monorepo Coherence...")
    # Pydantic boundary checks go here
    return {"sender": "schema-cop"}


# 3. The Orchestration Router
def routing_logic(state: SwarmState) -> str:
    # If SecOps finds a vulnerability, route back to Weaver
    if len(state.get("security_warnings", [])) > 0:
        return "weaver"
    # If linting/schemas fail, route back to Weaver
    if len(state.get("lint_errors", [])) > 0:
        return "weaver"
    # If the perimeter is clean, we are clear to push
    return "__end__"


# 4. Compile the Graph
builder = StateGraph(SwarmState)

builder.add_node("weaver", weaver_node)
builder.add_node("hound", hound_node)
builder.add_node("schema-cop", schema_cop_node)

# Define the swarm flow
builder.set_entry_point("weaver")
builder.add_edge("weaver", "hound")
builder.add_edge("hound", "schema-cop")

# Rely on dynamic string routing (type: ignore silences the false positive)
builder.add_conditional_edges("schema-cop", routing_logic)  # type: ignore

swarm_graph = builder.compile()

if __name__ == '__main__':
    print("[+] LangGraph State Machine Compiled and Ready.")
