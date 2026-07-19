from app.extensions import db
from app.base_model import BaseModel


class Recommendation(BaseModel):
    __tablename__ = "recommendations"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scheme_id = db.Column(
        db.Integer, db.ForeignKey("schemes.id", ondelete="CASCADE"), nullable=False, index=True
    )

    score = db.Column(db.Float, nullable=False, default=0.0)
    reason = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.UniqueConstraint("user_id", "scheme_id", name="uq_user_scheme_recommendation"),
        db.Index("ix_recommendations_user_score", "user_id", "score"),
    )

    def __repr__(self):
        return f"<Recommendation user_id={self.user_id} scheme_id={self.scheme_id} score={self.score}>"
