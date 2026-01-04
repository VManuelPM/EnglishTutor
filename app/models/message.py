from sqlalchemy import Column, Integer, String
from app.database.base import Base

class MessageHistory(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    original_text = Column(String)
    corrected_text = Column(String)
