import os
import pandas as pd

# =========================
# RAG SETUP
# =========================

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Load dataset
df = pd.read_csv("reviews.csv")

# Convert reviews into documents
documents = [Document(page_content=r) for r in df["review"]]

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector database
vector_db = Chroma.from_documents(documents, embeddings)

retriever = vector_db.as_retriever()

# Query RAG system
query = "customer complaints and positive feedback"
docs = retriever.invoke(query)

review_text = "\n".join([d.page_content for d in docs])


# =========================
# LLM SETUP (GROQ)
# =========================

from crewai import LLM

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.2
)


# =========================
# AGENTS
# =========================

from crewai import Agent

sentiment_agent = Agent(
    role="Sentiment Analyst",
    goal="Analyze whether customer reviews are positive or negative",
    backstory="Expert in analyzing product reviews and customer sentiment.",
    llm=llm
)

trend_agent = Agent(
    role="Market Trend Analyst",
    goal="Identify recurring complaints and praised product features",
    backstory="Specialist in extracting patterns in customer feedback.",
    llm=llm
)

report_agent = Agent(
    role="Business Strategist",
    goal="Generate a structured market insight report",
    backstory="Expert in summarizing analysis for business decision making.",
    llm=llm
)


# =========================
# TASKS
# =========================

from crewai import Task

sentiment_task = Task(
    description=f"""
Analyze the sentiment of the following product reviews.

Reviews:
{review_text}

Determine if the overall sentiment is positive, negative, or mixed.
Highlight key reasons behind the sentiment.
""",
    expected_output="A short paragraph summarizing the overall sentiment and key reasons.",
    agent=sentiment_agent
)

trend_task = Task(
    description=f"""
Identify common complaints and praised features in the following reviews.

Reviews:
{review_text}

Look for repeated patterns or themes mentioned by customers.
""",
    expected_output="A list of common complaints and most praised product features.",
    agent=trend_agent
)

report_task = Task(
    description="""
Using the outputs from the sentiment and trend analysis, generate a **detailed market analysis report in Markdown format**.

The report should be verbose and well structured.

Structure:

# Product Review Market Analysis Report

## Executive Summary
Provide a high level overview of the findings.

## Overall Sentiment Analysis
Explain whether sentiment is positive, negative or mixed.

## Key Customer Complaints
Explain major problems customers mention.

## Most Praised Product Features
Explain what customers love most.

## Market Trends and Patterns
Identify recurring themes in customer feedback.

## Business Insights
Explain what these findings mean for product strategy.

## Recommendations
Provide suggestions for product improvement.

Use clear headings, bullet points, and paragraphs.
""",
    expected_output="A detailed markdown formatted market analysis report.",
    agent=report_agent
)

# =========================
# CREW EXECUTION
# =========================
from crewai import Crew

crew = Crew(
    agents=[sentiment_agent, trend_agent, report_agent],
    tasks=[sentiment_task, trend_task, report_task],
    verbose=True
)

result = crew.kickoff()

report = str(result)

# Save report to Markdown file
with open("market_analysis_report.md", "w") as f:
    f.write(report)

print("\nReport saved to: market_analysis_report.md\n")