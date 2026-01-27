from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.common import common_router
from app.routers.orders import orders_router

origins = [
    "http://192.168.1.157:5173",
    "https://pizza42-spa-f7bb8ac15f77.herokuapp.com",
]

app = FastAPI(
    title="Pizza 42 Orders API",
    description="Backend API for Pizza 42 pizza orders",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"]
)

app.include_router(common_router)
app.include_router(orders_router)

