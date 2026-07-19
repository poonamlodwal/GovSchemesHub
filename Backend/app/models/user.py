from datetime import date

from app.extensions import db
from app.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(15), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    aadhaar_number = db.Column(db.String(12), nullable=True, unique=True, index=True)

    state = db.Column(db.String(100), nullable=True, index=True)
    district = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    annual_income = db.Column(db.Numeric(12, 2), nullable=True)
    category = db.Column(db.String(30), nullable=True)

    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    uploaded_documents = db.relationship(
        "UploadedDocument", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    recommendations = db.relationship(
        "Recommendation", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    notifications = db.relationship(
        "Notification", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    chat_history = db.relationship(
        "ChatHistory", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    audit_logs = db.relationship(
        "AuditLog", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.Index("ix_users_state_district", "state", "district"),
    )

    def calculate_age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])
        exclude.update({"password_hash"})
        return super().to_dict(exclude=exclude)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
