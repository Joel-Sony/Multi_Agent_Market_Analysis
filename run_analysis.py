"""
CLI Entry Point — Run the analysis from the command line.

Usage:
    python run_analysis.py
    python run_analysis.py --query "product quality and complaints"
"""

import argparse
from crew import run_analysis


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Market Analysis System (CrewAI + RAG)",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="customer complaints, positive feedback, and product quality",
        help="RAG retrieval query to find relevant reviews",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Multi-Agent Market Analysis System")
    print("  CrewAI + RAG Pipeline")
    print("=" * 60)

    result = run_analysis(query=args.query)

    print("\n" + "=" * 60)
    print("  ANALYSIS COMPLETE")
    print(f"  Report saved to: {result['saved_path']}")
    print("=" * 60)
    print("\n--- REPORT PREVIEW ---\n")
    print(result["report"][:2000])
    if len(result["report"]) > 2000:
        print(f"\n... ({len(result['report']) - 2000} more characters)")


if __name__ == "__main__":
    main()
