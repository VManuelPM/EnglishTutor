import os
import uuid
import chromadb
from sentence_transformers import SentenceTransformer
from fastapi.concurrency import run_in_threadpool

class VectorMemoryService:
    def __init__(self):
        # 1. Cargar el modelo de embeddings
        model_name = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)

        # 2. Persistencia en disco
        # Se guarda en la carpeta 'vector_db' en la raíz del proyecto
        self.client = chromadb.PersistentClient(path="./vector_db")

        # 3. Obtener o crear la colección de mensajes
        self.collection = self.client.get_or_create_collection(name="user_messages")

    async def add_message(self, user_id: str, message: str):
        """Traduce el mensaje a vectores y lo guarda de forma persistente."""
        if not message.strip():
            return

        # Generar embedding en un hilo separado para no bloquear el servidor
        embedding = await run_in_threadpool(self.model.encode, message)
        embedding_list = embedding.tolist()

        # Generar ID único para evitar colisiones
        unique_id = f"{user_id}_{uuid.uuid4()}"

        self.collection.add(
            ids=[unique_id],
            metadatas=[{"user_id": user_id, "message": message}],
            embeddings=[embedding_list]
        )

    async def get_relevant_messages(self, user_id: str, query: str, top_k=5):
        """Busca mensajes con significado similar a la consulta dentro del historial del usuario."""
        if not query.strip():
            return []

        # Traducir la consulta a vector
        query_emb = await run_in_threadpool(self.model.encode, query)
        query_emb_list = query_emb.tolist()

        # Consultar en ChromaDB filtrando por el ID del usuario
        results = self.collection.query(
            query_embeddings=[query_emb_list],
            n_results=top_k,
            where={"user_id": user_id}
        )

        # Extraer los mensajes de los metadatos obtenidos
        metadatas = results.get("metadatas")
        if metadatas and len(metadatas) > 0:
            return [m["message"] for m in metadatas[0] if m]
        return []
