import os
import chromadb
from typing import Dict, Any, List, Optional
from src.core.config import DB_PATH
from src.core.logger import logger

class MemoryEngine:
    def __init__(self) -> None:
        try:
            self.client = chromadb.PersistentClient(path=DB_PATH)
            self.collection = self.client.get_or_create_collection(
                name="oracle_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            logger.debug(f"🧠 [MEMORY] Connected to database at {DB_PATH}")
        
        except Exception as e:
            logger.critical(f"🔥 [MEMORY CRASH] Could not load database: {e}")

    def memorize(self, filename: str, content: str) -> None:
        """Saves file content into the vector database."""
        try:
            self.collection.upsert(
                documents=[content],
                metadatas=[{"filename": filename}],
                ids=[filename]
            )
            logger.info(f"✅ [MEMORY] Learned contents of '{filename}'")
        except Exception as e:
            logger.error(f"⚠️ [MEMORY ERROR] Failed to memorize {filename}: {e}")

    def forget(self, filename: str) -> None:
        """Removes a file from memory."""
        try:
            self.collection.delete(ids=[filename])
            logger.warning(f"🗑️ [MEMORY] Forgot '{filename}'")
        except Exception as e:
            logger.error(f"⚠️ [MEMORY ERROR] Failed to forget {filename}: {e}")

    def recall(self, query: str, n_results: int = 2) -> Dict[str, Any]:
        """Finds relevant code/text based on a query."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"⚠️ [MEMORY ERROR] Recall failed: {e}")
            return {'documents': [], 'metadatas': []}