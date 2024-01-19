import urllib
import uvicorn
from fastapi import FastAPI, Depends, Request
from typing import List
from src.routes.todo_items import router as todo_router
from src.routes.users import router as user_router
from src.models import todo
from src.database.auth import create_access_token
from src.database.db import get_db, engine, SessionLocal
from src.routes.adress_book import router as contact_router
from src.repo.adress_book import create_contact, get_contacts, get_contact_by_id, update_contact, delete_contact
from src.schemas.schemas import ContactCreate, ContactResponse  # Додано імпорт ContactResponse
from src.services.users import UserService

from fastapi_sso.sso.google import GoogleSSO

todo.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Підключення роутерів
app.include_router(contact_router, prefix="/api/v1")
app.include_router(todo_router, prefix="/todo")
app.include_router(user_router, prefix="/users")

GSSO_CLIENT_SECRET = "YOUR SECRET"
GSSO_CLIENT_ID = "YOUR CLIENT ID"


@app.get("/")
async def health_check():
    print()
    return {"OK": True}


def get_google_sso() -> GoogleSSO:
    return GoogleSSO(GSSO_CLIENT_ID, GSSO_CLIENT_SECRET, redirect_uri=REDIRECT_URI)


@app.get("/auth/google")
async def login_with_google():
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={urllib.parse.quote(GSSO_CLIENT_ID)}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope=openid%20profile%20email&response_type=code"
    return {"message": "Redirecting to Google for authentication...", "auth_url": google_auth_url}


@app.get("/google/callback")
async def complete_google_login(request: Request, google_sso: GoogleSSO = Depends(get_google_sso),
                                db: SessionLocal = Depends(get_db)):
    google_user = await google_sso.verify_and_process(request)

    user_service = UserService(db)
    user = user_service.get_by_username(google_user.email)
    access_token = create_access_token(username=user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}


REDIRECT_URI = "http://localhost:8000/google/callback"


def get_db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()


# Оголошення CRUD операцій
app.post("/api/v1/contacts/", response_model=ContactCreate)(create_contact)
app.get("/api/v1/contacts/", response_model=List[ContactResponse])(get_contacts)  # Виправлено імпорт
app.get("/api/v1/contacts/{contact_id}", response_model=ContactResponse)(get_contact_by_id)
app.put("/api/v1/contacts/{contact_id}", response_model=ContactCreate, response_model_exclude_unset=True)(
    update_contact)
app.delete("/api/v1/contacts/{contact_id}", response_model=None)(delete_contact)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
