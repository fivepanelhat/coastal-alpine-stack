import uuid
from swarm_state_machine import swarm_graph


def execute_test_run():
 print("[+] Initializing Sovereign Edge Swarm Test Run...")

 initial_state = {
 "target_file": "edge_auth.py",
 "code_content": "def login(u, p):\n if p == 'admin123':\n return True",
 "lint_errors": ["E225 missing whitespace around operator on line 2"],
 "security_warnings": ["B105:hardcoded_password_string found on line 2"],
 "revision_count": 0,
 "sender": "system"
 }

 # Define our persistent memory thread dynamically
 thread_id = f"secops-ticket-{str(uuid.uuid4())[:8]}"
 config = {"configurable": {"thread_id": thread_id}}

 # Execute with the config attached
 for event in swarm_graph.stream(initial_state, config): # type: ignore
 for node_name, state_update in event.items():
 if "code_content" in state_update:
 print("\n[!] Code Updated:")
 print("-" * 40)
 print(state_update['code_content'])
 print("-" * 40)


if __name__ == '__main__':
 execute_test_run()
