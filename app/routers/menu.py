from fastapi import APIRouter
from typing import List 

from app.models.pizza import Pizza

menu_router = APIRouter(prefix="/menu",tags=["Menu"])

menu: List[Pizza] = [
    Pizza(
        id=1,
        name="Margherita",
        price=12,
        description="Classic pizza with tomato sauce, mozzarella, and basil.",
        image_path="/images/pizzas/margherita.jpg",
    ),
    Pizza(
        id=2,
        name="Quattro Formaggi",
        price=13,
        description="Mozzarella, gorgonzola, parmesan, and goat cheese.",
        image_path="/images/pizzas/quattro-formaggi.jpg",
    ),
    Pizza(
        id=3,
        name="Regina",
        price=14,
        description="Tomato, mozzarella, ham, and mushrooms.",
        image_path="/images/pizzas/regina.jpg",
    ),
    Pizza(
        id=4,
        name="Calzone",
        price=15,
        description="Folded pizza stuffed with cheese, ham, and tomato sauce.",
        image_path="/images/pizzas/calzone.jpg",
    ),
    Pizza(
        id=5,
        name="Diavola",
        price=14,
        description="Tomato sauce, mozzarella, spicy salami, and chili flakes.",
        image_path="/images/pizzas/diavola.jpg",
    ),
    Pizza(
        id=6,
        name="Vegetariana",
        price=13,
        description="Tomato sauce, mozzarella, bell peppers, onions, olives, and mushrooms.",
        image_path="/images/pizzas/vegetariana.jpg",
    ),
    Pizza(
        id=7,
        name="Prosciutto e Funghi",
        price=14,
        description="Tomato sauce, mozzarella, prosciutto, and mushrooms.",
        image_path="/images/pizzas/prosciutto_e_funghi.jpg",
    ),
    Pizza(
        id=8,
        name="Hawaiana",
        price=13,
        description="Tomato sauce, mozzarella, ham, and pineapple.",
        image_path="/images/pizzas/hawaiana.jpg",
    ),
]

@menu_router.get("/", response_model=list[Pizza])
def get_menu():
    return (menu)