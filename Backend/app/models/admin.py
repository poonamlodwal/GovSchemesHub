from app.extensions import db
from app.base_model import BaseModel


class Admin(BaseModel):
    __tablename__ = "admins"

    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default="admin", nullable=False)

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])
        exclude.update({"password_hash"})
        return super().to_dict(exclude=exclude)

    def __repr__(self):
        return f"<Admin id={self.id} email={self.email} role={self.role}>"
