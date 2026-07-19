import uuid
from datetime import datetime
from app.extensions import db


class DocumentVerification(db.Model):
    __tablename__ = "document_verification"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey("uploaded_documents.id"), nullable=False, index=True)
    admin_id = db.Column(db.String(36), db.ForeignKey("admins.id"), nullable=True, index=True)

    verification_status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    verification_notes = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    document = db.relationship(
        "UploadedDocument", backref=db.backref("verification_records", lazy="dynamic", cascade="all, delete-orphan")
    )
    admin = db.relationship("Admin", backref=db.backref("verification_actions", lazy="dynamic"))

    __table_args__ = (
        db.Index("idx_docverify_document_status", "document_id", "verification_status"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "document_id": self.document_id,
            "admin_id": self.admin_id,
            "verification_status": self.verification_status,
            "verification_notes": self.verification_notes,
            "rejection_reason": self.rejection_reason,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<DocumentVerification {self.id} document={self.document_id}>"