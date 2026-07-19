from app.extensions import db
from app.base_model import BaseModel


class Scheme(BaseModel):
    __tablename__ = "schemes"

    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    eligibility_summary = db.Column(db.Text, nullable=True)
    application_process = db.Column(db.Text, nullable=True)
    official_link = db.Column(db.String(255), nullable=True)
    last_date = db.Column(db.Date, nullable=True)
    state = db.Column(db.String(100), nullable=True, index=True)

    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True
    )

    eligibility_rules = db.relationship(
        "EligibilityRule", backref="scheme", lazy="dynamic", cascade="all, delete-orphan"
    )
    required_documents = db.relationship(
        "RequiredDocument", backref="scheme", lazy="dynamic", cascade="all, delete-orphan"
    )
    recommendations = db.relationship(
        "Recommendation", backref="scheme", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Scheme id={self.id} title={self.title}>"
