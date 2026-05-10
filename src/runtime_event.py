import uuid
import time
from dataclasses import dataclass, field
from typing import List
from typing import List, Optional, Dict, Any

@dataclass
class RuntimeContext:
    run_id: str
    focus: str
    causal_depth: int = 0
    semantic_tags: List[str] = None
    actor: str = "unknown"
    scope_path: List[str] = None

    def __post_init__(self):
        if self.semantic_tags is None:
            self.semantic_tags = []
        if self.scope_path is None:
            self.scope_path = []

    def derive(self, focus: str, tag: str = None, actor: str = None) -> 'RuntimeContext':
        """Creates a child context for recursive lineage."""
        new_tags = list(self.semantic_tags)
        if tag:
            new_tags.append(tag)
        
        new_path = list(self.scope_path)
        new_path.append(self.focus)
        
        return RuntimeContext(
            run_id=self.run_id,
            focus=focus,
            causal_depth=self.causal_depth + 1,
            semantic_tags=new_tags,
            actor=actor or self.actor,
            scope_path=new_path
        )

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
