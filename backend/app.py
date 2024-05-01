from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from schema import TodoBase, TodoCreate, TodoUpdate
import model
import crud
import schema

from database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/todos", response_model=list[schema.Todo])
def read_todos(skip:int=0, limit:int=100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip, limit)
    return todos
    

@app.get("/todos/{id}", response_model=schema.Todo)
def read_todo(id: int, db: Session = Depends(get_db) ):
    todo = crud.get_todo_by_id(db, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found") 
    return todo

@app.post("/todos",response_model=schema.Todo)
def create_todo(item: TodoCreate, db: Session = Depends(get_db)):
    todo = crud.create_todo(db, item)
    if not todo:
        raise HTTPException(status_code=4000, detail="Todo not created")
    return todo

@app.put("/todos/{id}")
def update_todo(id: int, item: TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.get_todo_by_id(db, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo = crud.update_todo(db, id, item)
    return todo

@app.delete("/todos/{id}", response_model=schema.Todo)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo_by_id(db, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found") 
    todo = crud.delete_todo(db, id)
   
    return todo