from datetime import datetime

from app.extensions import db, bcrypt
from app.models.user import User


class AuthServiceError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


def register_user(data):
    email = data.get("email").strip().lower()
    phone = data.get("phone").strip()

    if User.query.filter_by(email=email).first():
        raise AuthServiceError("Email already registered", status_code=409)

    if User.query.filter_by(phone=phone).first():
        raise AuthServiceError("Phone number already registered", status_code=409)

    password_hash = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")

    date_of_birth = datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d").date()

    user = User(
        full_name=data.get("full_name").strip(),
        email=email,
        phone=phone,
        password_hash=password_hash,
        state=data.get("state").strip(),
        district=data.get("district").strip(),
        city=data.get("city").strip(),
        gender=data.get("gender").strip(),
        date_of_birth=date_of_birth,
        occupation=data.get("occupation").strip(),
        annual_income=float(data.get("annual_income")),
        category=data.get("category").strip(),
    )
    user.save()

    return user


def authenticate_user(identifier, password):
    identifier = (identifier or "").strip()

    user = User.query.filter(
        (User.email == identifier.lower()) | (User.phone == identifier)
    ).first()

    if not user:
        raise AuthServiceError("User not found", status_code=404)

    if user.is_deleted or not user.is_active:
        raise AuthServiceError("Account is not active", status_code=401)

    if not bcrypt.check_password_hash(user.password_hash, password or ""):
        raise AuthServiceError("Invalid credentials", status_code=401)

    user.last_login = datetime.utcnow()
    db.session.commit()

    return user


def get_current_user(user_id):
    user = User.get_by_id(user_id)
    if not user or user.is_deleted:
        raise AuthServiceError("User not found", status_code=404)
    return user
