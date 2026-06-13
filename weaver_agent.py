from typing import TYPE_CHECKING
from langchain_ollama import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

if TYPE_CHECKING:
    from swarm_state_machine import SwarmState

# ---------------------------------------------------------
# 1. Sovereign Edge Models & Vector Store
# ---------------------------------------------------------
# Using gemma4:latest as verified on the system
llm = ChatOllama(model="gemma4:latest", temperature=0.1)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Initialize local vector database
vector_store = Chroma(
    collection_name="sovereign_secops_memory",
    embedding_function=embeddings,
    persist_directory="./chroma_memory"
)

# ---------------------------------------------------------
# 2. Pydantic Edge Guard Schema
# ---------------------------------------------------------
class WeaverOutput(BaseModel):
    refactored_code: str = Field(
        description=(
            "The completely refactored, PEP-8 compliant Python code. "
            "Absolutely no markdown formatting or conversational text."
        )
    )

parser = PydanticOutputParser(pydantic_object=WeaverOutput)

# ---------------------------------------------------------
# 3. Vector-Augmented Prompt
# ---------------------------------------------------------
WEAVER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are Weaver, an elite Red Team SecOps AI agent. "
        "Fix the vulnerabilities. {format_instructions}"
    ),
    (
        "human",
        "Target: {target_file}\n"
        "Sec Warnings: {security_warnings}\n"
        "Lint Errors: {lint_errors}\n"
        "Historical Context:\n{historical_context}\n"
        "Code:\n{code_content}\n"
        "Provide the secure code."
    )
])

# Bind the prompt, LLM, and Pydantic parser together into an unbreakable chain
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

    if not sec_warn and not lint_err and code != "":
        return {"sender": "weaver"}

    # 1. Retrieve Historical Context (RAG)
    search_query = f"File: {target} Warnings: {' '.join(sec_warn)} Lint: {' '.join(lint_err)}"
    past_fixes = vector_store.similarity_search(search_query, k=1)

    context_str = "No relevant past fixes found."
    if past_fixes:
        context_str = f"In the past, you fixed a similar issue this way:\n{past_fixes[0].page_content}"

    # 2. Execute Inference
    response = invoke_local_llm({
        "target_file": target,
        "security_warnings": "\n".join(sec_warn) if sec_warn else "None",
        "lint_errors": "\n".join(lint_err) if lint_err else "None",
        "historical_context": context_str,
        "code_content": code,
        "format_instructions": parser.get_format_instructions()
    })

    # Extract the strictly parsed code from the Pydantic object
    safe_code = response.refactored_code

    # 3. Save the new fix to Long-Term Memory
    memory_payload = f"Issue: {sec_warn} {lint_err}\nSolution:\n{safe_code}"
    vector_store.add_texts(texts=[memory_payload], metadatas=[{"file": target}])

    return {
        "code_content": safe_code.strip(),
        "security_warnings": [],
        "lint_errors": [],
        "sender": "weaver",
        "revision_count": state.get("revision_count", 0) + 1
    }

