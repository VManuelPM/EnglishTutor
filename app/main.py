from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.routers import messages_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\nAplicación iniciando...", flush=True)
    # Startup: Base de Datos
    Base.metadata.create_all(bind=engine)

    # Startup: GPT
    # Importante: Esto descargará el modelo si no existe y PUEDE TARDAR MUCHO.
    messages_router.gpt_service.initialize()

    yield
    print("[LIFESPAN] Aplicación cerrándose...", flush=True)

app = FastAPI(lifespan=lifespan)
app.include_router(messages_router.router)
