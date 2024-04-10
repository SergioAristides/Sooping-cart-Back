from fastapi import FastAPI, Body, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Importa CORSMiddleware
from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, Field, validator, model_validator
from typing import Any, Optional, List
import os

from fastapi.staticfiles import StaticFiles

#################################################

tags_metadata = [
    {
        "name": "web",
        "description": "Endpoints of example",
    },
    {
        "name": "products",
        "description": "Product handling endpoints",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.title = "Product API"
app.summary = "Product REST API with FastAPI and Python"
app.description = "This is a demostration of API REST using Python"
app.version = "0.0.1"
app.contact = {
    "name": "Jorge I. Meza",
    "url": "https://co.linkedin.com/in/jimezam",
    "email": "jimezam@autonoma.edu.co",
} 

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Reemplaza con el origen de tu aplicación Vue
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#################################################
# Resto del código de tu aplicación FastAPI

#################################################

@app.get('/hello', 
         tags=["web"], 
         description="Shows an HTML hello world")
def greet():
    return HTMLResponse("<h1>Hello World</h1>")

#################################################

## Validation schemas

class Product (BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the product")
    name: str = Field(min_length=4, max_length=50, title="Name of the product")
    price: float = Field(default="1000", le=5000000, lg=100, title="Price of the product")
    expiration: Optional[str] = Field(default=None, title="Expiration date of the product")

    ## Advanced field validator

    @validator("name")
    @classmethod
    def validate_no_poison(cls, value):
        if value == "poison":
            raise ValueError("Posion should not be expended as product")
        return value
    
    ## Advanced multi-field validator

    @model_validator(mode='after')
    def validate_expensive_cheap_products(self):
        name = self.name
        price = self.price

        if name == "cheap" and price > 100000:
            raise ValueError("A product with that price cannot be named cheap.")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Platanitos",
                "price": 5000,
                "expiration": "2025-04-04"
            }
        }

images_directory = "C:/Users/Sergi/OneDrive/Desktop/cursosDiciembre/frontend/ApiProduct/Backend/DemoFastAPI-guia/images"

# Monta el directorio "images" como ruta estática "/images"
app.mount("/images", StaticFiles(directory=images_directory), name="images")

products = [
 {
        "id": 0,
        "name": "Papitas",
        "price": 30000,
        "expiration": "2025-01-01",
        "image": None,
        "brand":"margarita"
    },
    {
        "id": 1,
        "name": "Gomitas",
        "price": 25000,
        "expiration": "2025-01-01",
        "image": None,
        "brand":"trululu"
        
    },
    {
        "id": 2,
        "name": "Juguitos",
        "price": 300,
        "expiration": "2025-02-02",
        "image": None,
        "brand":"valle"
    },
    {
        "id": 3,
        "name": "Binos",
        "price": 2000,
        "image": None,
        "rating": 4.5,
        "brand": "Binos Inc.",
        "size": None
    },
    {
        "id": 4,
        "name": "Smartphone",
        "price": 800,
        "image": None,
        "rating": 4.0,
        "brand": "TechMaster",
        "size": None
    },
    {
        "id": 5,
        "name": "Laptop",
        "price": 1200,
        "image": None,
        "rating": 4.8,
        "brand": "ElectroTech",
        "size": None
    },
    {
        "id": 6,
        "name": "Camiseta",
        "price": 25,
        "image": None,
        "rating": 4.2,
        "brand": "FashionTees",
        "size": "M"
    },
    {
        "id": 7,
        "name": "Pantalón",
        "price": 40,
        "image": None,
        "rating": 4.3,
        "brand": "UrbanWear",
        "size": "L"
    },
    {
        "id": 8,
        "name": "Vestido",
        "price": 50,
        "image": None,
        "rating": 4.6,
        "brand": "ChicStyle",
        "size": "S"
    },
    {
        "id": 9,
        "name": "Zapatos de hombre",
        "price": 80,
        "image": None,
        "rating": 4.4,
        "brand": "FootMaster",
        "size": "42"
    },
    {
        "id": 10,
        "name": "Zapatos de mujer",
        "price": 70,
        "image": None,
        "rating": 4.7,
        "brand": "FashionFeet",
        "size": "38"
    },
    {
        "id": 11,
        "name": "Tablet",
        "price": 300,
        "image": None,
        "rating": 4.5,
        "brand": "TabTech",
        "size": None
    },
    {
        "id": 12,
        "name": "Reloj inteligente",
        "price": 150,
        "image": None,
        "rating": 4.2,
        "brand": "SmartTime",
        "size": None
    },
    {
        "id": 13,
        "name": "Gafas de sol",
        "price": 35,
        "image": None,
        "rating": 4.6,
        "brand": "SunShades",
        "size": None
    },
    {
        "id": 14,
        "name": "Bolso",
        "price": 60,
        "image": None,
        "rating": 4.3,
        "brand": "BagIt",
        "size": None
    },
    {
        "id": 15,
        "name": "Auriculares inalámbricos",
        "price": 90,
        "image": None,
        "rating": 4.8,
        "brand": "SoundMaster",
        "size": None
    }
]

## CRUD's endpoints definition

@app.get('/products', 
         tags=['products'], 
         response_model=List[Product], 
         description="Returns all products stored")
def get_all_products(min_price: float = Query(default=None, min=10, max=5000000), 
                     max_price: float = Query(default=None, min=10, max=5000000)) -> List[Product]:
    result = []
    for element in products:
        if(min_price is not None and element['price'] < min_price):
            continue
        if(max_price is not None and element['price'] > max_price):
            continue
        result.append(element)
    return JSONResponse(content=result, status_code=200)

@app.get('/products/{id}', 
         tags=['products'], 
         response_model=Product, 
         description="Returns data of one specific product")
def get_product(id: int = Path(ge=1, le=5000)) -> Product:
    for element in products:
        if element["id"] == id:
            return JSONResponse(content=element, status_code=200)
    return JSONResponse(content=None, status_code=404)

@app.post('/products', 
          tags=['products'], 
          response_model=dict, 
          description="Creates a new product")
def create_product(product: Product = Body()) -> dict:
    products.append(product.model_dump())
    return JSONResponse(content={
        "message": "The product was created successfully",
        "data": product.model_dump()
    }, status_code=201)

@app.put('/products/{id}', 
         tags=['products'], 
         response_model=dict, 
         description="Updates the data of specific product")
def update_product(id: int = Path(ge=1), 
                   product: Product = Body()) -> dict:
    for element in products:
        if element['id'] == id:
            element['name'] = product.name
            element['price'] = product.price
            element['expiration'] = product.expiration
            return JSONResponse(content={
                "message": "The product was updated successfully",
                "data": element
            }, status_code=200)
    return JSONResponse(content={
        "message": "The product does not exists",
        "data": None
    }, status_code=404)

@app.delete('/products/{id}', 
            tags=['products'], 
            response_model=dict, 
            description="Removes specific product")
def remove_product(id: int = Path(ge=1)) -> dict:
    for element in products:
        if element['id'] == id:
            products.remove(element)
            return JSONResponse(content={
                "message": "The product wass removed successfully",
                "data": None
            }, status_code=204)
    return JSONResponse(content={
        "message": "The product does not exists",
        "data": None
    }, status_code=404)



class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    

# Usuarios de prueba
test_users = [
    User(username="sergio", email="sriverabuitrago4@gmail.com", password="1234"),
    User(username="user2", email="user2@example.com", password="password2"),
    User(username="user3", email="user3@example.com", password="password3")
]

# Inicia la aplicación FastAPI

# Endpoint para obtener todos los usuarios
@app.get("/users/", response_model=List[User])
def get_users():
    return test_users
#################################################
