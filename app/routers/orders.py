from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi import Depends

from typing import List 

from app.models.order import Order, OrderCreate

from app.routers.menu import menu

from app.dependencies.auth_scheme import jwt_required

orders_router = APIRouter(prefix="/orders",tags=["Orders"])

orders : List[Order] = []
order_id_counter = 1

@orders_router.post("/")
def create_order(order_input: OrderCreate, payload:dict= Depends(jwt_required(scopes=["create:order"]))):
    global order_id_counter
    user_sub = payload.get("sub") 
    total_price = 0.0

    if not order_input.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must contain at least one element")
    
    for item in order_input.items:
        pizza = next( (p for p in menu if p.id == item.pizza_id), None)
        if pizza is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Pizza with id {item.pizza_id} does not exist")
        
        if item.quantity <=0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Item quantity must be greater than 0")

        total_price += pizza.price * item.quantity

    order = Order(
        id=order_id_counter,
        user_subject=user_sub,
        items=order_input.items,
        total_price=total_price,
    )

    order_id_counter += 1
    orders.append(order)

    return order


@orders_router.get("/")
def get_orders(payload:dict= Depends(jwt_required(scopes=["read:order"]))):
    return {"orders": orders}