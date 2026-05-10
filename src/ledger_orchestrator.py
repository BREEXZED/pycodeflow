import fcntl
import os
import json
from typing import Any
from src.runtime_event import RuntimeEvent

class LedgerOrchestrator:
    """
    Ensures metabolic integrity of the biographical ledger via advisory locks.
    Prevents race conditions in multi-agent event emission.
    """
    
    def __init__(self, log_path: str):
        self.log_path = log_path

    def atomic_append(self, event: RuntimeEvent):
        """Append an event to the ledger with a file-level write lock."""
        with open(self.log_path, 'a') as f:
            # Apply advisory lock
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                # Use to_dict() + json.dumps as RuntimeEvent doesn't have to_json
                f.write(json.dumps(event.to_dict()) + "\n")
                f.flush()
            finally:
                # Release lock
                fcntl.flock(f, fcntl.LOCK_UN)
