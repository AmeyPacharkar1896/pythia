import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import google.generativeai as genai
from src.config import DB_PATH, API_KEY

# Configure Embedding Model
genai.configure(api_key=API_KEY)

class GeminiEmbeddingFn(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Uses the specialized embedding model
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=input,
            task_type="retrieval_document",
            title="Oracle Document"
        )
        return response['embedding']

class MemoryEngine:
    def __init__(self):
        print("🧠 Initializing Vector Memory...")
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name="oracle_knowledge",
            embedding_function=GeminiEmbeddingFn()
        )

    def memorize(self, filename, text):
        """Saves text to the vector DB."""
        # Chunking limit (simple version)
        text_chunk = text[:8000] 
        try:
            self.collection.upsert(
                documents=[text_chunk],
                metadatas=[{"filename": filename}],
                ids=[filename]
            )
            print(f"   ✅ [MEMORY] Saved '{filename}' to database.")
        except Exception as e:
            print(f"   🛑 [MEMORY ERROR] {e}")

    def recall(self, query, n_results=3):
        """Retrieves relevant documents."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def forget(self, filename):
        """Removes a file from the vector database."""
        try:
            # We use the filename as the ID (since we kept it simple)
            self.collection.delete(ids=[filename])
            print(f"   🗑️ [MEMORY] Forgot '{filename}'")
        except Exception as e:
            # It's okay if we try to delete something that doesn't exist
            print(f"   ⚠️ [MEMORY] Could not forget '{filename}': {e}")