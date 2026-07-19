from app.extensions import db
from app.base_model import BaseModel


class RequiredDocument(BaseModel):
    __tablename__ = "required_documents"

    scheme_id = db.Column(
        db.Integer, db.ForeignKey("schemes.id", ondelete="CASCADE"), nullable=False, index=True
    )

    document_name = db.Column(db.String(150), nullable=False)
    is_required = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<RequiredDocument id={self.id} document_name={self.document_name}>"
