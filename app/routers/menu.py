from fastapi import APIRouter

menu_router = APIRouter(prefix="/menu",tags=["Menu"])

menu = [
    {
        "id": 1,
        "name": "Margherita",
        "price": 12,
        "description": "Classic pizza with tomato sauce, mozzarella, and basil.",
        "image_path": "/images/pizzas/margherita.jpg",
    },
    {
        "id": 2,
        "name": "Quattro Formaggi",
        "price": 13,
        "description": "Mozzarella, gorgonzola, parmesan, and goat cheese.",
        "image_path": "/images/pizzas/quattro-formaggi.jpg",
    },
    {
        "id": 3,
        "name": "Regina",
        "price": 14,
        "description": "Tomato, mozzarella, ham, and mushrooms.",
        "image_path": "/images/pizzas/regina.jpg",
    },
    {
        "id": 4,
        "name": "Calzone",
        "price": 15,
        "description": "Folded pizza stuffed with cheese, ham, and tomato sauce.",
        "image_path": "/images/pizzas/calzone.jpg",
    },
    {
        "id": 5,
        "name": "Diavola",
        "price": 14,
        "description": "Tomato sauce, mozzarella, spicy salami, and chili flakes.",
        "image_path": "/images/pizzas/diavola.jpg",
    },
    {
        "id": 6,
        "name": "Vegetariana",
        "price": 13,
        "description": "Tomato sauce, mozzarella, bell peppers, onions, olives, and mushrooms.",
        "image_path": "/images/pizzas/vegetariana.jpg",
    },
    {
        "id": 7,
        "name": "Prosciutto e Funghi",
        "price": 14,
        "description": "Tomato sauce, mozzarella, prosciutto, and mushrooms.",
        "image_path": "/images/pizzas/prosciutto_e_funghi.jpg",
    },
    {
        "id": 8,
        "name": "Hawaiana",
        "price": 13,
        "description": "Tomato sauce, mozzarella, ham, and pineapple.",
        "image_path": "/images/pizzas/hawaiana.jpg",
    },
]

@menu_router.get("/")
def get_menu():
    return (menu)