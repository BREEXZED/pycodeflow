from typing import Any, Dict, List
import sys
sys.path.append('/workspace/pycodeflow')
from src.runtime_event import RuntimeEvent, RuntimeContext
from src.causal_memory import EventStore
from src.core_analyzer import CoreAnalyzer
from src.semantic_registry import SemanticAnchor, Action, EventKind

class ReflectiveOrchestrator:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self.analyzer = CoreAnalyzer()
        self._context_stack: List[RuntimeContext] = []

    @property
    def current_context(self) -> RuntimeContext:
        return self._context_stack[-1] if self._context_stack else None

    def push_context(self, context: RuntimeContext):
        self._context_stack.append(context)

    def pop_context(self):
        if self._context_stack:
            self._context_stack.pop()

    def analyze_file_reflected(self, file_path: str, context: RuntimeContext = None) -> Dict[str, Any]:
        active_context = context or self.current_context
        if not active_context:
            raise ValueError("No context provided or available in stack")
            
        event = RuntimeEvent(
            event_type=EventKind.PARSE_START.value,
            subject=file_path,
            context=active_context,
            payload={"action": Action.SCAN.value}
        )
        self.event_store.append(event)
        
        try:
            result = self.analyzer.analyze(file_path)
            
            # Semantic Adaptation: derive context from analysis results
            category = result.get('file_info', {}).get('category', 'unknown')
            adapted_context = active_context.derive(focus=active_context.focus, tag=category)
            self.push_context(adapted_context)
            
            success_event = RuntimeEvent(
                parent_id=event.event_id,
                event_type=EventKind.PARSE_SUCCESS.value,
                subject=file_path,
                context=adapted_context,
                payload=result
            )
            self.event_store.append(success_event)
            return result
        except Exception as e:
            error_event = RuntimeEvent(
                parent_id=event.event_id,
                event_type=EventKind.PARSE_ERROR.value,
                subject=file_path,
                context=active_context,
                payload={"error": str(e)}
            )
            self.event_store.append(error_event)
            raise e
        finally:
            # Cleanup context hop
            if context is None:
                self.pop_context()
