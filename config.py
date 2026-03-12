"""
Centralized configuration for the Multi-Agent Market Analysis System.
Loads environment variables and defines project-wide constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM Configuration ─────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "groq/llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.2

# ── Embedding & Vector Store ──────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
CHROMA_COLLECTION = "market_reviews"

# ── Dataset ───────────────────────────────────────────────────────
DATASET_PATH = os.path.join(os.path.dirname(__file__), "reviews.csv")
SAMPLE_SIZE = 500  # Number of reviews to embed (keeps RAG fast)

# ── RAG Retrieval ─────────────────────────────────────────────────
RAG_TOP_K = 12  # Number of relevant docs to retrieve per query

# ── Output ────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Flask ─────────────────────────────────────────────────────────
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
