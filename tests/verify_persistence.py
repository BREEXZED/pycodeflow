import sys
import os
sys.path.append('/workspace/pycodeflow')

from src.causal_memory import EventStore

def verify_persistence():
    log_file = "/workspace/pycodeflow/output/event_log.jsonl"
    if os.path.exists(log_file):
        os.remove(log_file)
    
    # 1. Populate
    store = EventStore()
    from src.runtime_event import RuntimeEvent
    event = RuntimeEvent(event_type="TEST", subject="persist_test")
    store.append(event)
    
    # 2. Re-instantiate to trigger _load_and_index
    new_store = EventStore()
    
    # 3. Verify index
    indexed_events = new_store.get_by_subject("persist_test")
    print(f"Persistence Test: {'SUCCESS' if len(indexed_events) > 0 else 'FAILED'}")
    print(f"Found event ID: {indexed_events[0]['event_id'] if indexed_events else 'None'}")

verify_persistence()
