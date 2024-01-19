from fastapi import Depends
from sqlalchemy.orm import Session
from src.models.base import Contact
from src.database.db import get_db


async def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()


async def get_contact_by_id(contact_id: int, db: Session = Depends(get_db)):
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(contact_data: dict, db: Session = Depends(get_db)):
    contact = Contact(**contact_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, new_contact_data: dict, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    for key, value in new_contact_data.items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(contact)
    db.commit()
    return contact
