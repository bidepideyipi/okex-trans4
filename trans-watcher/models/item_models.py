"""
Item models for basic CRUD operations
"""

from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    """Base item model with common fields"""
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True


class ItemCreate(ItemBase):
    """Model for creating new items"""
    pass


class ItemUpdate(ItemBase):
    """Model for updating existing items"""
    name: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None


class Item(ItemBase):
    """Complete item model with ID"""
    id: Optional[int] = None

    class Config:
        from_attributes = True
