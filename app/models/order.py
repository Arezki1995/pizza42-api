from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    pizza_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]


class Order(BaseModel):
    id: int
    user_subject: str
    items: List[OrderItem]
    total_price: float
    timestamp: datetime
