from fastapi import APIRouter, Depends
from src.database.db import get_db, SessionLocal
from src.database.auth import create_access_token, DefaultUser
from src.schemas.user import User
from src.services.users import UserService
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/register/", response_model=User)
async def register(user: User, db: SessionLocal = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_new(user)


@router.get("/protected-resource/", response_model=User)
async def protected_resource(current_user: DefaultUser):
    return current_user
