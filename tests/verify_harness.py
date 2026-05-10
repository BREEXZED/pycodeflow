import sys
import os

# Add src to path so we can import our new modules
sys.path.append('/workspace/pycodeflow')

from src.causal_memory import EventStore
from src.orchestrator import ReflectiveOrchestrator
from src.api_interface import QueryEngine

from src.runtime_event import RuntimeContext

def verify_life():
    print("--- Starting Proof of Life Test ---")
    
    # 1. Setup
    store = EventStore(output_dir="/workspace/pycodeflow/output")
    orch = ReflectiveOrchestrator(store)
    query = QueryEngine(store)
    
    test_file = "/workspace/pycodeflow/tests/dummy_code/test_file.py"
    context = RuntimeContext(run_id="test_run_01", focus="verify_harness")
    
    # 2. Run analysis
    print(f"Analyzing: {test_file}")
    orch.analyze_file_reflected(test_file, context=context)
    
    # 3. Query events
    events = query.trace(test_file)
    print(f"Captured {len(events)} events for {os.path.basename(test_file)}:")
    for e in events:
        print(f"  [{e['event_type']}] ID: {e['event_id']}, Parent: {e.get('parent_id')}")
        
    # 4. Trace the 'WHY' (Find parent of success event)
    success_event = next((e for e in events if e['event_type'] == 'AST_PARSE_SUCCESS'), None)
    if success_event:
        why = query.why(success_event['event_id'])
        print(f"Trace WHY (parent) for SUCCESS event: {why[0]['event_type'] if why else 'None'}")
    
    print("--- Proof of Life Test Complete ---")

if __name__ == "__main__":
    verify_life()
