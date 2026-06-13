import logging
from typing import TYPE_CHECKING
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from tenacity import retry, stop_after_attempt, wait_exponential

if TYPE_CHECKING:
    from swarm_state_machine import SwarmState

logger = logging.getLogger("SovereignSwarm")

# ---------------------------------------------------------
# 1. THE PYDANTIC GUARD: Strict Output Schema
# ---------------------------------------------------------
class WeaverResponse(BaseModel):
    refactored_code: str = Field(description="The fully refactored, secure Python code. MUST NOT contain markdown formatting backticks.")
    security_cleared: bool = Field(description="True if all security warnings were resolved.")
    lint_cleared: bool = Field(description="True if all linting errors were resolved.")

# ---------------------------------------------------------
# 2. Local Sovereign Edge LLM (Forced JSON Mode)
# ---------------------------------------------------------
# By setting format="json", we force Ollama to strictly adhere to JSON structures
# Using gemma4:latest as verified on the system
llm = ChatOllama(model="gemma4:latest", temperature=0.1, format="json")

# Initialize the aggressive Pydantic parser
parser = PydanticOutputParser(pydantic_object=WeaverResponse)

# ---------------------------------------------------------
# 3. Mathematically Bound System Prompt
# ---------------------------------------------------------
WEAVER_PROMPT = PromptTemplate(
    template=(
        "You are Weaver, an elite Red Team SecOps AI agent.\n"
        "Fix the vulnerabilities and lint errors in the provided code.\n"
        "{format_instructions}\n\n"
        "File: {target_file}\n"
        "Sec Warnings: {security_warnings}\n"
        "Lint Errors: {lint_errors}\n"
        "Code:\n{code_content}\n"
    ),
    input_variables=["target_file", "security_warnings", "lint_errors", "code_content"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# The Execution Chain
weaver_chain = WEAVER_PROMPT | llm | parser

# ---------------------------------------------------------
# 4. The Titanium Wrapper
# ---------------------------------------------------------
@retry(
    stop=stop_after_attempt(5), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def invoke_local_llm(payload):
    return weaver_chain.invoke(payload)

# ---------------------------------------------------------
# 5. The Agent Node
# ---------------------------------------------------------
def autonomous_weaver_node(state: "SwarmState"):
    target = state.get("target_file", "unknown.py")
    code = state.get("code_content", "")
    sec_warn = state.get("security_warnings", [])
    lint_err = state.get("lint_errors", [])
    
    # Check if perimeter is clear
    if not sec_warn and not lint_err and code != "":
        return {"sender": "weaver"}

    logger.info(f"Refactoring {target} (Attempt {state.get('revision_count', 0) + 1})...")

    try:
        # Execute inference through the Titanium Wrapper
        # The output is mathematically guaranteed to be a WeaverResponse object
        response: WeaverResponse = invoke_local_llm({
            "target_file": target,
            "security_warnings": "\n".join(sec_warn) if sec_warn else "None",
            "lint_errors": "\n".join(lint_err) if lint_err else "None",
            "code_content": code
        })
        
        logger.info(f"Pydantic Validation Passed. Output perfectly structured.")
        
        return {
            "code_content": response.refactored_code.strip(),
            "security_warnings": [],
            "lint_errors": [],
            "sender": "weaver",
            "revision_count": state.get("revision_count", 0) + 1
        }
    except Exception as e:
        err_msg = f"Weaver LLM/Pydantic Parsing Error: {str(e)}"
        logger.error(err_msg)
        return {"sender": "weaver", "agent_errors": state.get("agent_errors", []) + [err_msg]}

if __name__ == '__main__':
    logger.info("Weaver Agent Module Compiled.")
