from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.message_schemas import Message, MessageResponse, MessageHistoryResponse
from app.database.crud import messages_crud
from app.database.session import SessionLocal
from app.services.grammar_service import LanguageToolService
from app.services.gpt_service import GPTService

router = APIRouter()
grammar_service = LanguageToolService()
gpt_service = GPTService()  # Instancia única del GPTService

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sendMessage", response_model=MessageResponse)
async def send_message(msg: Message, db: Session = Depends(get_db)):
    # Lógica de corrección de texto
    corrected, _feedback = await grammar_service.check_text(msg.text)

    # Guardar historial
    messages_crud.create_message(db, msg.user_id, msg.text, corrected)

    # Generar respuesta GPT de forma asíncrona
    try:
        gpt_reply = await gpt_service.generate_reply(msg.user_id, db, msg.text)
    except Exception:
        gpt_reply = "Lo siento, no puedo responder a tu mensaje ahora."

    return MessageResponse(original=msg.text, corrected=corrected, message=gpt_reply)


@router.get("/history/{user_id}", response_model=List[MessageHistoryResponse])
def get_history(user_id: str, db: Session = Depends(get_db)):
    messages = messages_crud.get_history_by_user(db, user_id)
    return [
        MessageHistoryResponse(original=m.original_text, corrected=m.corrected_text)
        for m in messages
    ]
