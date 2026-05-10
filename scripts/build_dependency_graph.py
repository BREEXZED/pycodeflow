import sys
import os
import json
sys.path.append('/workspace/pycodeflow')

from src.causal_memory import EventStore

def build_graph():
    store = EventStore()
    events = store.get_events()
    
    graph = {}
    
    print("--- Building Master Dependency Graph ---")
    for e in events:
        if e['event_type'] == 'AST_PARSE_SUCCESS':
            subject = e['subject']
            payload = e['payload']
            
            # Extract imports (keys are module names)
            imports = list(payload.get('imports', {}).keys())
            
            graph[subject] = {
                "imports": imports,
                "io_ops": len(payload.get('io_operations', [])),
                "funcs": list(payload.get('function_usage', {}).keys())
            }
            
    print(json.dumps(graph, indent=2))
    return graph

if __name__ == "__main__":
    build_graph()
