from datetime import datetime

from app.extensions import db
from app.base_model import BaseModel


class UploadedDocument(BaseModel):
    __tablename__ = "uploaded_documents"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    document_name = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    verification_status = db.Column(db.String(20), default="pending", nullable=False, index=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.Index("ix_uploaded_docs_user_status", "user_id", "verification_status"),
    )

    def __repr__(self):
        return f"<UploadedDocument id={self.id} user_id={self.user_id} status={self.verification_status}>"
