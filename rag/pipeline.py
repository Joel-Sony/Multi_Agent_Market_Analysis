"""
RAG Pipeline — Embedding, Vector Store & Retrieval.

Loads the review dataset, builds a ChromaDB vector store with
HuggingFace sentence embeddings, and exposes a retrieval function
that the CrewAI agents use to fetch contextually relevant reviews.
"""

import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from config import (
    DATASET_PATH,
    EMBEDDING_MODEL,
    CHROMA_PERSIST_DIR,
    SAMPLE_SIZE,
    RAG_TOP_K,
)

# ── Module-level cache ────────────────────────────────────────────
_vector_db = None
_dataframe = None

# Active dataset path (defaults to the original reviews.csv)
ACTIVE_DATASET_PATH = DATASET_PATH

def set_active_dataset(filepath: str) -> None:
    """Set a new active dataset and clear RAG caches."""
    global ACTIVE_DATASET_PATH, _dataframe, _vector_db
    ACTIVE_DATASET_PATH = filepath
    _dataframe = None
    _vector_db = None


def load_dataset() -> pd.DataFrame:
    """Load and cache the review dataset."""
    global _dataframe
    if _dataframe is None:
        _dataframe = pd.read_csv(ACTIVE_DATASET_PATH)
    return _dataframe


def get_dataset_stats() -> dict:
    """Return basic statistics about the dataset."""
    df = load_dataset()
    class_counts = df["class"].value_counts().to_dict()
    return {
        "total_reviews": len(df),
        "positive_reviews": int(class_counts.get(1, 0)),
        "negative_reviews": int(class_counts.get(0, 0)),
        "avg_review_length": int(df["review"].str.len().mean()) if len(df) > 0 else 0,
        "max_review_length": int(df["review"].str.len().max()) if len(df) > 0 else 0,
        "min_review_length": int(df["review"].str.len().min()) if len(df) > 0 else 0,
    }


def _build_vector_db() -> Chroma:
    """Build (or return cached) ChromaDB vector store."""
    global _vector_db
    if _vector_db is not None:
        return _vector_db

    df = load_dataset()
    sampled = df.sample(n=min(SAMPLE_SIZE, len(df)), random_state=42)

    documents = [
        Document(
            page_content=row["review"],
            metadata={"class": int(row["class"])},
        )
        for _, row in sampled.iterrows()
    ]

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Use a dynamic collection name based on the dataset to separate embeddings
    import hashlib
    file_hash = hashlib.md5(ACTIVE_DATASET_PATH.encode()).hexdigest()[:8]
    collection_name = f"market_reviews_{file_hash}"

    _vector_db = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
        collection_name=collection_name,
    )
    return _vector_db


def retrieve_reviews(query: str, top_k: int = RAG_TOP_K) -> str:
    """
    Retrieve the most relevant reviews for a given query.
    Returns concatenated review text.
    """
    db = _build_vector_db()
    retriever = db.as_retriever(search_kwargs={"k": top_k})
    docs = retriever.invoke(query)
    return "\n---\n".join(doc.page_content for doc in docs)
