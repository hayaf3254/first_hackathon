from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base

class FoodCategory(Base):
    __tablename__ = "food_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False) 
    parent_id = Column(Integer, ForeignKey('food_categories.id'), nullable=True)

    parent = relationship("FoodCategory", remote_side=[id], back_populates="children")
    children = relationship("FoodCategory", back_populates="parent")