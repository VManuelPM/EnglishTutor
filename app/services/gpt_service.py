import os
import logging
from dotenv import load_dotenv
from gpt4all import GPT4All
from app.database.crud import messages_crud
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool
from app.services.vector_memory_service import VectorMemoryService

load_dotenv()
logger = logging.getLogger("uvicorn.error")

MODEL_NAME = os.getenv("MODEL_NAME", "Meta-Llama-3-8B-Instruct.Q4_0.gguf")


class GPTService:
    def __init__(self, vector_service: VectorMemoryService = None):
        self.model = None
        # Si no se pasa un servicio, lo creamos (Inyección de dependencias)
        self.vector_memory = vector_service or VectorMemoryService()

    def initialize(self):
        # Verifica la existencia del modelo y lo carga/descarga.
        if self.model is not None:
            return
        logger.info(f"GPTService: Verificando/Descargando modelo {MODEL_NAME}...")
        try:
            # Esto iniciará la descarga si no existe. 
            self.model = GPT4All(MODEL_NAME)
            logger.info("GPTService: Modelo cargado y listo.")
        except Exception as e:
            logger.error(f"GPTService: Error al cargar el modelo: {e}")
            raise e

    async def generate_reply(self, user_id: str, db: Session, user_message: str) -> str:
        if self.model is None:
            self.initialize()

        # 1. Recuperar contexto reciente (SQL)
        history = messages_crud.get_history_by_user(db, user_id)
        recent_context = "\n".join([
            f"User: {h.original_text} | Tutor: {h.corrected_text}"
            for h in history[-5:]
        ])

        # 2. Recuperar memoria semántica (Vectores)
        relevant_messages = await self.vector_memory.get_relevant_messages(user_id, user_message)
        vector_context = "\n- ".join(relevant_messages)

        # 3. Prompt estructurado (Más profesional)
        prompt = f"""
    ### System:
    You are an expert and empathetic English teacher. Your goal is to help the student improve their fluency and grammar.
    Strictly follow this response format:
    [Your response in English, greeting and continuing the conversation]

    Teacher's Note: [Brief technical explanation of the error committed, if any]

    ### Recent conversation context:
    {recent_context}

    ### Previously mentioned errors or topics:
    - {vector_context}

    ### Current student message:
    "{user_message}"

    ### Instructions:
    1. Analyze if the message has grammatical errors.
    2. Respond to the student naturally in English.
    3. If there was an error, add a brief section at the end called "Teacher's Note" explaining the correction.

    ### Teacher Response (Write only the response):
"""

        # 4. Generación asíncrona
        # En GPT4All, el parámetro para limitar tokens es n_predict
        response = await run_in_threadpool(
            self.model.generate,
            prompt,
            n_predict=250,
            temp=0.3,
        )

        # 5. Guardar en memoria inteligente para el futuro
        await self.vector_memory.add_message(user_id, user_message)

        return response
