from sqlalchemy.orm import Session
from app.models.message import MessageHistory

def create_message(db: Session, user_id: str, original_text: str, corrected_text: str):
    message = MessageHistory(
        user_id=user_id,
        original_text=original_text,
        corrected_text=corrected_text
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_history_by_user(db: Session, user_id: str):
    return db.query(MessageHistory).filter(MessageHistory.user_id == user_id).all()
