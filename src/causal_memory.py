import json
import os
import fcntl
from typing import List, Dict, Any, Optional
from .runtime_event import RuntimeEvent
from src.ledger_orchestrator import LedgerOrchestrator

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

class EventStore:
    def __init__(self, output_dir: str = "/workspace/pycodeflow/output"):
        self.output_dir = output_dir
        self.log_path = os.path.join(output_dir, "event_log.jsonl")
        self.ledger = LedgerOrchestrator(self.log_path)
        self.events = []
        self.event_by_id = {}
        self.events_by_subject = {}
        if os.path.exists(self.log_path):
            self._load_and_index()

    def _load_and_index(self):
        with open(self.log_path, 'r') as f:
            for line in f:
                event = json.loads(line)
                self.events.append(event)
                self.event_by_id[event['event_id']] = event
                subject = event.get('subject', 'root')
                self.events_by_subject.setdefault(subject, []).append(event)

    def append(self, event: RuntimeEvent):
        self.ledger.atomic_append(event)
        
        event_dict = event.to_dict()
        self.events.append(event_dict)
        self.event_by_id[event_dict['event_id']] = event_dict
        subject = event_dict.get('subject', 'root')
        self.events_by_subject.setdefault(subject, []).append(event_dict)

    def get_events(self): return self.events
    def get_by_id(self, eid): return self.event_by_id.get(eid)
    def get_by_subject(self, sub): return self.events_by_subject.get(sub, [])
