from app.extensions import db
from app.base_model import BaseModel


class ChatHistory(BaseModel):
    __tablename__ = "chat_history"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<ChatHistory id={self.id} user_id={self.user_id}>"
