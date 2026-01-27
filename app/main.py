from fastapi import FastAPI

from app.routers.common import common_router
from app.routers.orders import orders_router



app = FastAPI(
    title="Pizza 42 Orders API",
    description="Backend API for Pizza 42 pizza orders",
    version="1.0.0"
)

app.include_router(common_router)
app.include_router(orders_router)

