from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserRegister, UserLogin
from auth_utils import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register-user")
def register_user(user: UserRegister, db: Session = Depends(get_db)):

    hashed = hash_password(user.user_password)

    new_user = User(
        user_first_name=user.user_first_name,
        user_last_name=user.user_last_name,
        user_email=user.user_email,
        user_password=hashed
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(login: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.user_email == login.user_email).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(login.user_password, user.user_password):
        return {"error": "Invalid password"}

    return {
        "user_id": user.user_id,
        "email": user.user_email,
        "message": "Login successful"
    }