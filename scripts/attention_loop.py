import os
import json
import time
import subprocess
from src.causal_memory import EventStore

class AttentionLoop:
    """
    Autonomous loop monitoring the biographical ledger for 'high-entropy' 
    events to trigger reactive FocusScans.
    """
    def __init__(self, watch_interval=30):
        self.store = EventStore()
        self.watch_interval = watch_interval

    def _is_high_entropy(self, event):
        # Heuristic: AST_PARSE_ERROR or frequent SUCCESS in a short window
        return event['event_type'] in ['AST_PARSE_ERROR']

    def run(self):
        print("--- Attention Loop Active: Monitoring Ledger ---")
        last_processed_id = None
        
        while True:
            events = self.store.get_events()
            if not events:
                time.sleep(self.watch_interval)
                continue
                
            # Find new events
            if last_processed_id:
                try:
                    idx = next(i for i, e in enumerate(events) if e['event_id'] == last_processed_id)
                    new_events = events[idx+1:]
                except StopIteration:
                    new_events = events
            else:
                new_events = events

            for event in new_events:
                if self._is_high_entropy(event):
                    print(f"[!] High entropy detected in {event['subject']}: {event['event_type']}")
                    # Trigger surgical scan
                    subprocess.run(["python3", "main.py", "scan", event['subject']])
                
                last_processed_id = event['event_id']
            
            time.sleep(self.watch_interval)

if __name__ == "__main__":
    loop = AttentionLoop()
    loop.run()
