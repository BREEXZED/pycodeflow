import sys
sys.path.append('/workspace/pycodeflow')
from src.causal_memory import EventStore
from src.api_interface import QueryEngine

store = EventStore()
query = QueryEngine(store)

# This tests impact downstream of our test file
impact = query.impact("/workspace/pycodeflow/tests/dummy_code/test_file.py")
print(f"Impact detected: {len(impact)} downstream events found.")
