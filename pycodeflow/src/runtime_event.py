import uuid
import time
from dataclasses import dataclass, field
from typing import List
from typing import Dict, Any, Optional

@dataclass
class RuntimeContext:
    run_id: str
    focus: str
    causal_depth: int = 0
    semantic_tags: List[str] = field(default_factory=list)

@dataclass
class RuntimeEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None
    event_type: str = "GENERIC"
    subject: str = "root"
    timestamp: float = field(default_factory=time.time)
    payload: Dict[str, Any] = field(default_factory=dict)
    context: Optional[RuntimeContext] = None  # Full object capture

    def to_dict(self):
        d = self.__dict__.copy()
        if self.context:
            d['context'] = self.context.__dict__
        return d
