import sys
import os
sys.path.append('/workspace/pycodeflow')

from src.causal_memory import EventStore
from src.orchestrator import ReflectiveOrchestrator
from src.runtime_event import RuntimeContext

class FocusScanner:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self.orch = ReflectiveOrchestrator(event_store)

    def scan(self, target_file: str, run_id: str):
        """
        Surgically parse a target and its dependencies only.
        """
        ctx = RuntimeContext(run_id=run_id, focus=target_file)
        
        # 1. Analyze the target
        print(f"Scanning target: {target_file}")
        try:
            result = self.orch.analyze_file_reflected(target_file, ctx)
        except Exception as e:
            print(f"Error scanning {target_file}: {e}")
            return

        # 2. Extract dependencies from our event log's semantic data
        # 'imports' keys are the modules we need to scan next
        imports = result.get('imports', {})
        print(f"Found {len(imports)} dependencies to evaluate.")
        
        for module in imports:
            # Simple heuristic: if it's a file path or local module, we scan it.
            # In a real system, we'd use a PathResolver.
            potential_path = f"/workspace/pycodeflow/reference/original/{module}.py"
            if os.path.exists(potential_path):
                print(f"  -> Dependency found: {module}. Scanning...")
                self.orch.analyze_file_reflected(potential_path, ctx)

if __name__ == "__main__":
    store = EventStore()
    scanner = FocusScanner(store)
    target = "/workspace/pycodeflow/reference/original/gui.py"
    scanner.scan(target, run_id="focus_scan_01")
