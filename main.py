import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import src.database.models
from src.database.db import get_db
from src.routes.adress_book import router as contact_router
from src.repository.adress_book import create_contact, get_contacts, get_contact_by_id, update_contact, delete_contact
from src.schemas import ContactCreate
from src.database.models import Contact
from typing import List, Dict

app = FastAPI()

# Підключення роутерів
app.include_router(contact_router, prefix="/api/v1")


def get_db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()


# Оголошення CRUD операцій
app.post("/api/v1/contacts/", response_model=ContactCreate)(create_contact)
app.get("/api/v1/contacts/", response_model=Dict[str, src.schemas.ContactResponse])(get_contacts)
app.get("/api/v1/contacts/{contact_id}", response_model=Contact)(get_contact_by_id)
app.put("/api/v1/contacts/{contact_id}", response_model=ContactCreate)(update_contact)
app.delete("/api/v1/contacts/{contact_id}", response_model=None)(delete_contact)

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
