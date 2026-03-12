"""
Crew Orchestration — Assembles agents and tasks into a CrewAI Crew.

Provides the `run_analysis()` function that executes the full pipeline:
RAG retrieval → agent collaboration → strategic report.
"""

import os
from datetime import datetime
from crewai import Crew, LLM

from config import LLM_MODEL, LLM_TEMPERATURE, OUTPUT_DIR
from rag.pipeline import retrieve_reviews
from agents.definitions import (
    create_sentiment_agent,
    create_trend_agent,
    create_competitor_agent,
    create_strategist_agent,
)
from tasks.definitions import (
    create_sentiment_task,
    create_trend_task,
    create_competitor_task,
    create_report_task,
)


def _create_llm() -> LLM:
    """Create the LLM instance used by all agents."""
    return LLM(model=LLM_MODEL, temperature=LLM_TEMPERATURE)


def run_analysis(query: str = "customer complaints, positive feedback, and product quality") -> dict:
    """
    Execute the full multi-agent analysis pipeline.

    Args:
        query: The RAG retrieval query to find relevant reviews.

    Returns:
        dict with keys: 'report', 'timestamp', 'query', 'saved_path'
    """
    # ── Step 1: Retrieve relevant reviews via RAG ─────────────────
    print(f"\n🔍 Retrieving relevant reviews for: '{query}'")
    review_text = retrieve_reviews(query)
    print(f"✅ Retrieved relevant reviews\n")

    # ── Step 2: Initialize LLM and agents ─────────────────────────
    llm = _create_llm()

    sentiment_agent = create_sentiment_agent(llm)
    trend_agent = create_trend_agent(llm)
    competitor_agent = create_competitor_agent(llm)
    strategist_agent = create_strategist_agent(llm)

    # ── Step 3: Create tasks ──────────────────────────────────────
    sentiment_task = create_sentiment_task(sentiment_agent, review_text)
    trend_task = create_trend_task(trend_agent, review_text)
    competitor_task = create_competitor_task(competitor_agent, review_text)
    report_task = create_report_task(strategist_agent)

    # ── Step 4: Assemble and run crew ─────────────────────────────
    crew = Crew(
        agents=[sentiment_agent, trend_agent, competitor_agent, strategist_agent],
        tasks=[sentiment_task, trend_task, competitor_task, report_task],
        verbose=True,
    )

    print("🚀 Launching multi-agent crew...\n")
    result = crew.kickoff()
    report = str(result)

    # ── Step 5: Save report ───────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        f.write(report)

    print(f"\n📄 Report saved to: {filepath}")

    return {
        "report": report,
        "timestamp": timestamp,
        "query": query,
        "saved_path": filepath,
    }
