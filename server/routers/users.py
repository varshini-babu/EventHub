from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["Users"])


# Get user profile
@router.get("/profile/{userId}")
def get_user_profile(userId: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.user_id == userId).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.user_id,
        "user_first_name": user.user_first_name,
        "user_last_name": user.user_last_name,
        "user_email": user.user_email
    }


# Get single user
@router.get("/{userId}")
def get_user(userId: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.user_id == userId).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.user_id,
        "user_first_name": user.user_first_name,
        "user_last_name": user.user_last_name,
        "user_email": user.user_email
    }


# Delete user
@router.delete("/delete/{userId}")
def delete_user(userId: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.user_id == userId).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}