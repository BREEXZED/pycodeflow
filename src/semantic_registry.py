from enum import Enum
from typing import Dict, Any, TypedDict, List, Set

class Action(Enum):
    SCAN = "scan"
    REFLECT = "reflect"
    QUERY = "query"

class EventKind(Enum):
    PARSE_START = "AST_PARSE_START"
    PARSE_SUCCESS = "AST_PARSE_SUCCESS"
    PARSE_ERROR = "AST_PARSE_ERROR"

class PayloadKind(Enum):
    IMPORTS = "imports"
    IO_OPS = "io_operations"
    FUNC_USAGE = "function_usage"
    ERROR = "error"

class SemanticAnchor:
    """
    Defines the structural anatomy of the organism's perception.
    """
    ACTIONS = [a.value for a in Action]
    EVENT_KINDS = [e.value for e in EventKind]
    PAYLOAD_KINDS = [p.value for p in PayloadKind]
