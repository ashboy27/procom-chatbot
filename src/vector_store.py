import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
import faiss
import numpy as np

class VectorStore:
    """Simple vector store using SQLite + FAISS for local development."""

    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = db_path
        self.index = None
        self.embeddings = []
        self.chunks = []
        self._init_db()

    def _init_db(self):
       
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                metadata TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        if not faiss:
            raise ImportError("faiss-cpu is required. Install with: pip install faiss-cpu")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM chunks")
        conn.commit()

        for i, chunk in enumerate(chunks):
            metadata = json.dumps(chunk.get("metadata", {}))
            cursor.execute(
                "INSERT INTO chunks (content, metadata) VALUES (?, ?)",
                (chunk["content"], metadata),
            )

        conn.commit()
        conn.close()
        embeddings_np = np.array(embeddings, dtype=np.float32)
        dimension = embeddings_np.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_np)
        self.embeddings = embeddings_np

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.index:
            return []

        query_np = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_np, min(top_k, self.index.ntotal))

        results = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for idx in indices[0]:
            cursor.execute("SELECT content, metadata FROM chunks WHERE rowid = ?", (int(idx) + 1,))
            row = cursor.fetchone()
            if row:
                results.append({
                    "content": row[0],
                    "metadata": json.loads(row[1]) if row[1] else {},
                })

        conn.close()
        return results

    def clear(self):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chunks")
        conn.commit()
        conn.close()
        self.index = None
        self.embeddings = []
