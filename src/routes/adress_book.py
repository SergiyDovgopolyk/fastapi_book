from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from src.database.models import Contact
from src.database.db import get_db
from src.schemas import ContactCreate  # Додано імпорт схеми

router = APIRouter()


# Операція створення нового контакту
@router.post("/contacts/", response_model=ContactCreate)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Операція отримання списку всіх контактів
@router.get("/contacts/")
def get_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Contact).offset(skip).limit(limit).all()


# Операція отримання контакту за id
@router.get("/contacts/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# Операція оновлення контакту за id
@router.put("/contacts/{contact_id}", response_model=ContactCreate)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in contact.dict().items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Операція видалення контакту за id
@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}


# Операція пошуку контактів за ім'ям, прізвищем чи адресою електронної пошти
@router.get("/contacts/search/")
def search_contacts(query: str = Query(None, min_length=3), db: Session = Depends(get_db)):
    db_contacts = db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()
    return db_contacts


# Операція отримання списку контактів з днями народження на найближчі 7 днів
@router.get("/contacts/birthdays/")
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)
    upcoming_birthdays = db.query(Contact).filter(
        (Contact.birth_date >= today) & (Contact.birth_date <= end_date)
    ).all()
    return upcoming_birthdays
