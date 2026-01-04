from pydantic import BaseModel, Field

#Request
class Message(BaseModel):
    user_id: str
    text: str = Field(..., min_length=1)

#Response
class MessageResponse(BaseModel):
    original: str
    corrected: str
    message: str

class MessageHistoryResponse(BaseModel):
    original: str
    corrected: str