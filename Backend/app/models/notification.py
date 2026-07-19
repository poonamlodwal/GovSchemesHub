from app.extensions import db
from app.base_model import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)

    __table_args__ = (
        db.Index("ix_notifications_user_read", "user_id", "is_read"),
    )

    def __repr__(self):
        return f"<Notification id={self.id} user_id={self.user_id} is_read={self.is_read}>"
