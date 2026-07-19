from app.extensions import db
from app.base_model import BaseModel


class EligibilityRule(BaseModel):
    __tablename__ = "eligibility_rules"

    scheme_id = db.Column(
        db.Integer, db.ForeignKey("schemes.id", ondelete="CASCADE"), nullable=False, index=True
    )

    rule_name = db.Column(db.String(100), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False, index=True)
    rule_value = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.Index("ix_eligibility_scheme_rule_type", "scheme_id", "rule_type"),
    )

    def __repr__(self):
        return f"<EligibilityRule id={self.id} scheme_id={self.scheme_id} rule_type={self.rule_type}>"
