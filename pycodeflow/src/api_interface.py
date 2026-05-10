from typing import List, Dict, Any, Optional
from .causal_memory import EventStore

class QueryEngine:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def _filter_run(self, events: List[Dict[str, Any]], run_id: Optional[str]) -> List[Dict[str, Any]]:
        if not run_id: return events
        return [e for e in events if e.get('context', {}).get('run_id') == run_id]

    def trace(self, subject: str, run_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """TRACE: Find events related to subject, optionally scoped to a run_id."""
        events = self.event_store.get_by_subject(subject)
        return self._filter_run(events, run_id)

    def why(self, event_id: str, run_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """WHY: Navigate parent lineage, scoped to run_id."""
        lineage = []
        current_id = event_id
        while current_id:
            parent = self.event_store.get_by_id(current_id)
            if not parent: break
            
            # Context check
            if run_id and parent.get('context', {}).get('run_id') != run_id:
                break
                
            lineage.append(parent)
            current_id = parent.get("parent_id")
        return lineage

    def impact(self, subject: str, run_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """IMPACT: Find downstream events, scoped to run_id."""
        events = self.event_store.get_events()
        # Scope by run_id first if provided
        if run_id:
            events = self._filter_run(events, run_id)
            
        initial_events = [e for e in events if e.get('subject') == subject]
        queue = [e['event_id'] for e in initial_events]
        
        impacted = []
        processed = set()
        
        while queue:
            pid = queue.pop(0)
            if pid in processed: continue
            processed.add(pid)
            
            children = [e for e in events if e.get("parent_id") == pid]
            for child in children:
                impacted.append(child)
                queue.append(child['event_id'])
        return impacted

class AgentInterface:
    def __init__(self, event_store: EventStore):
        self.query = QueryEngine(event_store)
        
    def reflect(self, command: str, subject: str, run_id: Optional[str] = None) -> Any:
        cmd = command.upper()
        if cmd == "TRACE": return self.query.trace(subject, run_id)
        elif cmd == "IMPACT": return self.query.impact(subject, run_id)
        elif cmd == "WHY": return self.query.why(subject, run_id)
        return {"error": "Unknown command"}
