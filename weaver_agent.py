from typing import TYPE_CHECKING
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

if TYPE_CHECKING:
    from swarm_state_machine import SwarmState

# 1. Initialize the Local Inference Engine (Sovereign Edge)
# We default to gemma or phi3 for fast, local edge execution
llm = ChatOllama(model="gemma:2b", temperature=0.1)

# 2. Define the System Prompt
WEAVER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are Weaver, an elite Red Team SecOps AI agent. Your job is to write highly secure, PEP-8 compliant Python code for an edge computing environment. NEVER use plain text passwords. Always validate inputs. You will receive existing code and error reports. Output ONLY the corrected raw Python code. No markdown formatting, no explanations."),
    ("human", "Target File: {target_file}\n\nSecurity Warnings (Fix immediately): {security_warnings}\n\nLint Errors (Fix formatting): {lint_errors}\n\nCurrent Code:\n{code_content}\n\nRewrite the code to resolve all issues.")
])

# 3. Build the Chain
weaver_chain = WEAVER_PROMPT | llm


def autonomous_weaver_node(state: "SwarmState"):
    print("\n[Weaver] Analyzing state and firing local inference engine...")

    # Extract the current operational context
    target = state.get("target_file", "unknown.py")
    code = state.get("code_content", "")
    sec_warn = state.get("security_warnings", [])
    lint_err = state.get("lint_errors", [])

    # If the code is perfectly clean, do not waste NPU cycles rewriting it
    if not sec_warn and not lint_err and code != "":
        print("[Weaver] Perimeter is secure. No refactor required.")
        return {"sender": "weaver"}

    print(f"[Weaver] Refactoring {target} to clear {len(sec_warn)} security warnings and {len(lint_err)} linting errors...")

    # Execute the local LLM
    response = weaver_chain.invoke({
        "target_file": target,
        "security_warnings": "\n".join(sec_warn) if sec_warn else "None",
        "lint_errors": "\n".join(lint_err) if lint_err else "None",
        "code_content": code
    })

    # Update the swarm state with the newly minted secure code
    # We clear the errors array because Weaver believes it has fixed them;
    # Hound and Schema-Cop will re-verify on the next pass.
    return {
        "code_content": response.content.strip(),
        "security_warnings": [],
        "lint_errors": [],
        "sender": "weaver",
        "revision_count": state.get("revision_count", 0) + 1
    }


if __name__ == '__main__':
    print("[+] Weaver Agent Module Compiled.")
