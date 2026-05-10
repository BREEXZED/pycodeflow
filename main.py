import sys
import argparse
from src.causal_memory import EventStore
from src.orchestrator import ReflectiveOrchestrator
from src.runtime_event import RuntimeContext
from src.focus_scan import FocusScanner
from src.api_interface import AgentInterface

def main():
    parser = argparse.ArgumentParser(description="Reflective Execution Harness CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Surgically scan a module and its dependencies")
    scan_parser.add_argument("target", help="File path to scan")
    scan_parser.add_argument("--run-id", default="cli_run", help="Unique ID for this session")

    # Reflect command
    reflect_parser = subparsers.add_parser("reflect", help="Query causal history")
    reflect_parser.add_argument("verb", choices=["TRACE", "WHY", "IMPACT"])
    reflect_parser.add_argument("subject", help="File or entity to query")
    reflect_parser.add_argument("--run-id", help="Filter by run ID")

    args = parser.parse_args()
    store = EventStore()
    
    if args.command == "scan":
        scanner = FocusScanner(store)
        scanner.scan(args.target, args.run_id)
        print(f"Scan complete. Run ID: {args.run_id}")

    elif args.command == "reflect":
        agent = AgentInterface(store)
        result = agent.reflect(args.verb, args.subject, args.run_id)
        print(f"Reflection result ({args.verb}):")
        print(result)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
