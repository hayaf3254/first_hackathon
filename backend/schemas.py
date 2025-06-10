from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field

class FoodCategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class FoodCategoryCreate(FoodCategoryBase):
    pass

class FoodCategory(FoodCategoryBase):
    id: int
    class Config:
        from_attributes = True