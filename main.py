from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.crud import create_item, get_items, get_item, update_item, delete_item

app = FastAPI()

class TodoItem(BaseModel):
    itemId: str
    title: str
    description: Optional[str] | None = None
    done: bool = False
 


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI DynamoDB Todo App!"}

@app.get("/items/", response_model=List[TodoItem])
def read_todo_items():
    return get_items()

@app.post("/items", response_model=TodoItem)
def create_todo_item(item: TodoItem):
    created_item = create_item(item.model_dump())
    return created_item  # Ensure that create_item returns the item itself


@app.get("/items/{item_id}", response_model=TodoItem)
def read_todo_item(item_id: str):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=TodoItem)
def update_todo_item(item_id: str, updates: TodoItem):
    item = update_item(item_id, updates.model_dump())
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}", response_model=dict)
def delete_todo_item(item_id: str):
    response = delete_item(item_id)
    if 'ResponseMetadata' not in response:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
