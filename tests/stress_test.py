import sys
import os
sys.path.append('/workspace/pycodeflow')

from src.causal_memory import EventStore
from src.orchestrator import ReflectiveOrchestrator
from src.api_interface import AgentInterface
from src.runtime_event import RuntimeContext

def stress_test():
    store = EventStore()
    orch = ReflectiveOrchestrator(store)
    agent = AgentInterface(store)
    
    # Define a complex context
    ctx = RuntimeContext(run_id="stress_01", focus="main.py")
    
    # Analyze files
    files = [
        "/workspace/pycodeflow/tests/dummy_code/test_file.py",
        "/workspace/pycodeflow/reference/original/analyzer.py"
    ]
    
    for f in files:
        if os.path.exists(f):
            orch.analyze_file_reflected(f, ctx)
            
    # Test Agent Interface Queries
    print("Agent Interface Stress Test:")
    print("1. TRACE test_file.py:", agent.reflect("TRACE", files[0]))
    print("2. WHY trace for success events (first 1):")
    events = store.get_events()
    success = next((e for e in events if e['event_type'] == 'AST_PARSE_SUCCESS'), None)
    if success:
        print(agent.reflect("WHY", success['event_id']))
    print("3. IMPACT of analyzer.py (if any):")
    print(agent.reflect("IMPACT", files[1]))

stress_test()
