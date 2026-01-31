from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.common import common_router
from app.routers.orders import orders_router
from app.routers.menu import menu_router

from pathlib import Path
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent

origins = [
    "http://localhost:5173",
    "https://pizza42-spa-f7bb8ac15f77.herokuapp.com",
]

app = FastAPI(
    title="Pizza 42 API",
    description="Backend API for Pizza 42",
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
app.include_router(menu_router)
app.include_router(orders_router)

app.mount(
    "/images",
    StaticFiles(directory=BASE_DIR / "images"),
    name="images",
)