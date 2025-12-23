from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter(prefix="/products", 
                   tags= ["products"],# tags es para agrupar las rutas en la documentacion
                   responses={404: {"message": "Not found"}})
# Levantar servidor local
# uvicorn products:app --reload
    
# products_list = ["Producto 1", "Producto 2", "Producto 3"]
class Product(BaseModel):
    id: int
    name: str
    stock: int


products_lista = [
    Product(id=1, name="apple", stock=10),
    Product(id=2, name="orange", stock=10),
]

@router.get("/")
async def products():
    return products

@router.get("/{id}")
async def product(id: int):
    return searc_user(id)


def searc_user(id: int):
    for product in products_lista:
        product.id == id
        return product
    return {"error": "Product not found"}

