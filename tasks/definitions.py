"""
CrewAI Task Definitions.

Each task represents a discrete analytical step. Tasks are created
as factory functions that accept the assigned agent and context data.
"""

from crewai import Task


def create_sentiment_task(agent, review_text: str) -> Task:
    """Task: Analyze sentiment of retrieved reviews."""
    return Task(
        description=f"""\
Perform a detailed sentiment analysis of the following customer reviews.

────────────────────────────────────────
REVIEWS:
{review_text}
────────────────────────────────────────

Your analysis MUST include:
1. Overall sentiment classification (Positive / Negative / Mixed)
2. Estimated sentiment ratio (e.g., 70% positive, 30% negative)
3. Top 3 drivers of positive sentiment (with example quotes)
4. Top 3 drivers of negative sentiment (with example quotes)
5. Any notable emotional patterns (frustration, delight, surprise, etc.)
""",
        expected_output=(
            "A structured sentiment analysis with classification, ratio, "
            "key drivers with quotes, and emotional patterns."
        ),
        agent=agent,
    )


def create_trend_task(agent, review_text: str) -> Task:
    """Task: Identify trends and patterns in reviews."""
    return Task(
        description=f"""\
Analyze the following customer reviews to identify recurring trends and patterns.

────────────────────────────────────────
REVIEWS:
{review_text}
────────────────────────────────────────

Your analysis MUST include:
1. Top 5 most common COMPLAINTS (ranked by frequency)
2. Top 5 most PRAISED features/aspects (ranked by frequency)
3. Emerging trends or shifts in customer expectations
4. Any seasonal, temporal, or demographic patterns you detect
5. Feature requests or unmet needs mentioned by customers
""",
        expected_output=(
            "A ranked list of complaints and praised features, plus "
            "emerging trends and unmet customer needs."
        ),
        agent=agent,
    )


def create_competitor_task(agent, review_text: str) -> Task:
    """Task: Extract competitive intelligence from reviews."""
    return Task(
        description=f"""\
Examine the following reviews for competitive intelligence insights.

────────────────────────────────────────
REVIEWS:
{review_text}
────────────────────────────────────────

Your analysis MUST include:
1. Any direct or indirect mentions of competitor products/services
2. Comparison language used by customers (better than, worse than, etc.)
3. Competitive advantages the product/service has based on reviews
4. Competitive gaps or weaknesses relative to market expectations
5. Market positioning summary
""",
        expected_output=(
            "A competitive intelligence brief covering competitor mentions, "
            "advantages, gaps, and market positioning."
        ),
        agent=agent,
    )


def create_report_task(agent) -> Task:
    """Task: Generate the final strategic market analysis report."""
    return Task(
        description="""\
Using ALL the outputs from the sentiment analysis, trend identification, \
and competitive intelligence tasks, generate a **comprehensive, executive-ready \
market analysis report in Markdown format**.

The report MUST follow this structure:

# 📊 Market Analysis Report

## Executive Summary
A high-level overview of the key findings (3-4 sentences).

## Sentiment Analysis
- Overall sentiment classification and ratio
- Key positive and negative drivers
- Emotional patterns

## Customer Complaints & Pain Points
- Ranked list of top complaints
- Root cause analysis where possible
- Impact assessment

## Praised Features & Strengths
- Ranked list of most praised aspects
- What customers value most

## Market Trends & Patterns
- Emerging trends
- Shifting customer expectations
- Unmet needs

## Competitive Landscape
- Market positioning
- Competitive advantages and gaps

## Strategic Recommendations
- Prioritized, actionable recommendations (at least 5)
- Quick wins vs. long-term initiatives
- Expected impact of each recommendation

## Conclusion
Summary of the most critical takeaways.

Use clear headings, bullet points, bold text for emphasis, and tables where appropriate. \
Make the report detailed, insightful, and actionable.
""",
        expected_output=(
            "A comprehensive, well-structured Markdown market analysis report "
            "covering all sections listed above."
        ),
        agent=agent,
    )
