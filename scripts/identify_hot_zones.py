import sys
import os
import json
sys.path.append('/workspace/pycodeflow')

from src.causal_memory import EventStore

def identify_hot_zones():
    store = EventStore()
    events = store.get_events()
    
    # Analyze files for "entropy"
    # Criteria: number of I/O operations + number of unique module imports
    hot_zones = []
    
    for e in events:
        if e['event_type'] == 'AST_PARSE_SUCCESS':
            subject = e['subject']
            payload = e['payload']
            
            # Extract metrics
            io_count = len(payload.get('io_operations', []))
            imports = payload.get('imports', {})
            import_count = len(imports)
            
            entropy = io_count + import_count
            
            hot_zones.append({
                "file": subject,
                "entropy": entropy,
                "io_count": io_count,
                "import_count": import_count
            })
            
    # Sort by entropy descending
    hot_zones.sort(key=lambda x: x['entropy'], reverse=True)
    
    print("--- High-Entropy Module Analysis ---")
    for zone in hot_zones[:10]:
        print(f"File: {os.path.basename(zone['file'])}")
        print(f"  Entropy: {zone['entropy']} (IO: {zone['io_count']}, Imports: {zone['import_count']})")
        print("-" * 30)

if __name__ == "__main__":
    identify_hot_zones()
