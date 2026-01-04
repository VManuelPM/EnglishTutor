import os
import logging
from dotenv import load_dotenv
from gpt4all import GPT4All
from app.database.crud import messages_crud
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool

load_dotenv()
logger = logging.getLogger("uvicorn.error")

MODEL_NAME = os.getenv("MODEL_NAME", "Meta-Llama-3-8B-Instruct.Q4_0.gguf")


class GPTService:
    def __init__(self):
        self.model = None

    def initialize(self):
        #Verifica la existencia del modelo y lo carga/descarga.
        if self.model is not None:
            return
        logger.info(f"GPTService: Verificando/Descargando modelo {MODEL_NAME}...")
        try:
            # Esto iniciará la descarga si no existe. 
            # El progreso de gpt4all debería salir en consola ahora.
            self.model = GPT4All(MODEL_NAME)
            logger.info("GPTService: Modelo cargado y listo.")
        except Exception as e:
            logger.error(f"GPTService: Error al cargar el modelo: {e}")
            raise e

    async def generate_reply(self, user_id: str, db: Session, user_message: str) -> str:
        """
        Genera la respuesta del chatbot basada en el historial del usuario y su mensaje actual.
        """
        # Recuperar historial del usuario
        history = messages_crud.get_history_by_user(db, user_id)
        context = ""

        # Últimos 5 mensajes (o menos si no hay tantos)
        for h in history[-5:]:
            context += f"Original: {h.original_text}\nCorrected: {h.corrected_text}\n"

        # Preparar prompt
        prompt = f"""
Eres un profesor de inglés. Tu alumno ha enviado el siguiente mensaje:
{user_message}

Historial reciente del usuario:
{context}

Corrige y explica de forma amable si es necesario. Responde en inglés.
"""

        # Ejecutar la generación en un thread pool para no bloquear el event loop
        response = await run_in_threadpool(self.model.generate, prompt)
        return response
