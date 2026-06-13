from typing import TYPE_CHECKING
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential

if TYPE_CHECKING:
    from swarm_state_machine import SwarmState

# 1. Local Sovereign Edge LLM
llm = ChatOllama(model="gemma:2b", temperature=0.1)

# 2. System Prompt
WEAVER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are Weaver, an elite Red Team SecOps AI agent. Write secure, "
        "PEP-8 Python. Output ONLY raw code."
    ),
    (
        "human",
        "File: {target_file}\n"
        "Sec Warnings: {security_warnings}\n"
        "Lint Errors: {lint_errors}\n"
        "Code:\n{code_content}\n"
        "Rewrite to resolve issues."
    )
])

weaver_chain = WEAVER_PROMPT | llm


# 3. THE TITANIUM WRAPPER: Exponential Backoff for NPU Resilience
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def invoke_local_llm(payload):
    return weaver_chain.invoke(payload)


# 4. The Agent Node
def autonomous_weaver_node(state: "SwarmState"):
    target = state.get("target_file", "unknown.py")
    code = state.get("code_content", "")
    sec_warn = state.get("security_warnings", [])
    lint_err = state.get("lint_errors", [])

    # Check if perimeter is clear
    if not sec_warn and not lint_err and code != "":
        return {"sender": "weaver"}

    print(f"[Weaver] Refactoring {target} (Attempt {state.get('revision_count', 0) + 1})...")

    # Execute inference through the Titanium Wrapper
    response = invoke_local_llm({
        "target_file": target,
        "security_warnings": "\n".join(sec_warn) if sec_warn else "None",
        "lint_errors": "\n".join(lint_err) if lint_err else "None",
        "code_content": code
    })

    response_content = response.content
    if isinstance(response_content, list):
        content_str = "".join([
            chunk.get("text", str(chunk)) if isinstance(chunk, dict) else str(chunk)
            for chunk in response_content
        ])
    else:
        content_str = str(response_content)

    return {
        "code_content": content_str.strip(),
        "security_warnings": [],
        "lint_errors": [],
        "sender": "weaver",
        "revision_count": state.get("revision_count", 0) + 1
    }


if __name__ == '__main__':
    print("[+] Weaver Agent Module Compiled.")
