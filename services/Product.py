import copy

from models.models import Product as product_model
from DTO.Product import Product as product_dto
from DTO.User import User as user_dto

from fastapi import HTTPException


def create_product(data: product_dto, db):
    product = product_model(name=data.name, amount=data.amount, description=data.description, price=data.price,
                            isVisible=data.isVisible)

    try:
        db.add(product)


    except Exception as e:
        print(e)

    return product


def get_product(id: int, db):
    product = db.query(product_model).filter(product_model.id == id).first()
    if product is None:
        raise HTTPException(status_code=400, detail="No such product id in the product list")
    return product


def get_all_products(db):
    return db.query(product_model).all()


def get_products(db):
    return db.query(product_model).filter(product_model.isVisible == True).all()


def update_price(id: int, price: int, db):
    product = get_product(id, db)
    product.price = price

    return product


def update_amount(id: int, amount: int, db):
    product = get_product(id, db)
    product.amount = amount
    return product

def delete_product(id: int, db):
    product = get_product(id, db)
    db.delete(product)
    return product


def update_description(id: int, description: str, db):
    product = get_product(id, db)
    product.description = description

    return product


def update_visibility(id: int, isVisible: bool, db):
    product = get_product(id, db)
    product.isVisible = isVisible

    return product
