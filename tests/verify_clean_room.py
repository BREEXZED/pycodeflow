import sys
sys.path.append('/workspace/pycodeflow')
from src.causal_memory import EventStore
from src.orchestrator import ReflectiveOrchestrator
from src.api_interface import AgentInterface
from src.runtime_event import RuntimeContext

def verify_clean_room():
    store = EventStore()
    orch = ReflectiveOrchestrator(store)
    agent = AgentInterface(store)
    
    test_file = "/workspace/pycodeflow/tests/dummy_code/test_file.py"
    
    # 1. Run two distinct sessions
    ctx1 = RuntimeContext(run_id="run_A", focus="main.py")
    ctx2 = RuntimeContext(run_id="run_B", focus="main.py")
    
    orch.analyze_file_reflected(test_file, ctx1)
    orch.analyze_file_reflected(test_file, ctx2)
    
    # 2. Query scoped
    results_A = agent.reflect("TRACE", test_file, run_id="run_A")
    results_B = agent.reflect("TRACE", test_file, run_id="run_B")
    
    print(f"Run A events: {len(results_A)}")
    print(f"Run B events: {len(results_B)}")
    
    # 3. Verify isolation
    if len(results_A) == 2 and len(results_B) == 2:
        print("Clean Room Test: SUCCESS - Runs are isolated.")
    else:
        print("Clean Room Test: FAILED - Cross-run contamination detected.")

verify_clean_room()
