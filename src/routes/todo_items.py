from fastapi import APIRouter, Depends
from src.schemas.schemas import Todo, TodoCreate, TodoUpdate
from src.schemas.user import User
from src.database.db import get_db, SessionLocal
from src.services.todo import TodoService

from src.database.auth import AdminUser, DefaultUser, Manager

router = APIRouter()


@router.get("/")
async def list_todos(user: DefaultUser, db: SessionLocal = Depends(get_db)) -> list[Todo]:
    todo_items = TodoService(db=db).get_all_todos()
    return todo_items


@router.get("/{id}")
async def get_detail(id: int, user: DefaultUser, db: SessionLocal = Depends(get_db))-> Todo:
    todo_item = TodoService(db=db).get_by_id(id)
    return todo_item


@router.post("/")
async def create_todo(todo_item: TodoCreate, admin: AdminUser, db: SessionLocal = Depends(get_db)) -> Todo:
    new_item = TodoService(db=db).create_new(todo_item)
    return new_item


@router.put("/{id}")
async def update_todo(id: int, todo_item: TodoUpdate, db: SessionLocal = Depends(get_db)) -> Todo:
    updated_item = TodoService(db=db).update(todo_item)
    return updated_item
