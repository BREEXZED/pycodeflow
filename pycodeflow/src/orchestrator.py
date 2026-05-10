from typing import Any, Dict
import sys
sys.path.append('/workspace/pycodeflow')
from reference.original.analyzer import analyze_file
from src.runtime_event import RuntimeEvent, RuntimeContext
from src.causal_memory import EventStore

class ReflectiveOrchestrator:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def analyze_file_reflected(self, file_path: str, context: RuntimeContext) -> Dict[str, Any]:
        event = RuntimeEvent(
            event_type="AST_PARSE_START",
            subject=file_path,
            context=context,
            payload={"action": "analyze_file_start"}
        )
        self.event_store.append(event)
        
        try:
            result = analyze_file(file_path)
            # The result is exactly the structure we want to log
            success_event = RuntimeEvent(
                parent_id=event.event_id,
                event_type="AST_PARSE_SUCCESS",
                subject=file_path,
                context=context,
                payload=result  # Log the FULL dictionary
            )
            self.event_store.append(success_event)
            return result
        except Exception as e:
            error_event = RuntimeEvent(
                parent_id=event.event_id,
                event_type="AST_PARSE_ERROR",
                subject=file_path,
                context=context,
                payload={"error": str(e)}
            )
            self.event_store.append(error_event)
            raise e
