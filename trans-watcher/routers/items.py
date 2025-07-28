"""
Items router for basic CRUD operations
"""

from fastapi import APIRouter, HTTPException
from typing import List
from models import Item, ItemCreate

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage (for demo purposes)
items_db = []
next_id = 1


@router.get("/", response_model=List[Item])
async def get_items():
    """Get all items"""
    return items_db


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get item by ID"""
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/", response_model=Item)
async def create_item(item: ItemCreate):
    """Create new item"""
    global next_id
    new_item = item.dict()
    new_item["id"] = next_id
    next_id += 1
    items_db.append(new_item)
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """Update item"""
    for i, existing_item in enumerate(items_db):
        if existing_item["id"] == item_id:
            updated_item = item.dict()
            updated_item["id"] = item_id
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """Delete item"""
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            deleted_item = items_db.pop(i)
            return {"message": f"Item {item_id} deleted successfully", "deleted_item": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/search/{query}", response_model=List[Item])
async def search_items(query: str):
    """Search items by name"""
    results = [item for item in items_db if query.lower() in item["name"].lower()]
    return results
