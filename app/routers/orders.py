from fastapi import APIRouter

orders_router = APIRouter(prefix="/orders",tags=["Orders"])


@orders_router.post("/")
def create_order():
    return {"message": "Order received (not protected yet)"}


@orders_router.get("/")
def get_orders():
    return {"orders": []}