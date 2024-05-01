from sqlalchemy.orm import Session
import model
import schema

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Todo).offset(skip).limit(limit).all()

def get_todo_by_id(db: Session, id: int):
    return db.query(model.Todo).filter(model.Todo.id == id).first()

def create_todo(db: Session, todo: schema.TodoCreate):
    db_todo = model.Todo(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, id: int, todo: schema.TodoUpdate):
    db_todo = db.query(model.Todo).filter(model.Todo.id == id).first()
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, id: int):
    db_todo = db.query(model.Todo).filter(model.Todo.id == id).first()
    db.delete(db_todo)
    db.commit()
    return db_todo