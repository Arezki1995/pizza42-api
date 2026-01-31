from pydantic import BaseModel


class Pizza(BaseModel):
    id: int
    name: str
    price: float
    description: str
    image_path: str

