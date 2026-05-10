import sys
import os
sys.path.append('/workspace/pycodeflow')

from src.causal_memory import EventStore
from src.orchestrator import ReflectiveOrchestrator
from src.api_interface import AgentInterface
from src.runtime_event import RuntimeContext

def run_deep_analysis():
    store = EventStore()
    orch = ReflectiveOrchestrator(store)
    agent = AgentInterface(store)
    
    # Analyze the main components of the reference organism
    target_files = [
        "/workspace/pycodeflow/reference/original/analyzer.py",
        "/workspace/pycodeflow/reference/original/dependency_store.py",
        "/workspace/pycodeflow/reference/original/gui.py"
    ]
    
    ctx = RuntimeContext(run_id="deep_analysis_01", focus="analyzer.py")
    
    print(f"--- Starting Reflective Analysis of Reference Organism ---")
    for f in target_files:
        if os.path.exists(f):
            print(f"Analyzing: {os.path.basename(f)}")
            try:
                orch.analyze_file_reflected(f, ctx)
            except Exception as e:
                print(f"  Handled error in {f}: {e}")
    
    print("\n--- Analysis Complete. Reflecting on evidence: ---")
    # Query the harness for insights
    for f in target_files:
        events = agent.reflect("TRACE", f, run_id="deep_analysis_01")
        print(f"\nSubject: {os.path.basename(f)}")
        for e in events:
            payload = e.get('payload', {})
            print(f"  [{e['event_type']}] {payload.get('code_segment', '') or payload.get('summary', 'No summary')[:50]}...")

if __name__ == "__main__":
    run_deep_analysis()
