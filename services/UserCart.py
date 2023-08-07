import json

from models.models import UserCart as cart_model
from DTO.User import User as user_dto

from fastapi import HTTPException


def create_cart(user: user_dto, db):
    cart = cart_model(items="{}", total_price=0, user_id=user.id)

    try:
        db.add(cart)
        db.commit()
        db.refresh(cart)

    except Exception as e:
        print(e)

    return cart


def get_cart(user: user_dto, db) -> cart_model:
    return db.query(cart_model).filter(cart_model.user_id == user.id).first()


def add_item(user: user_dto, product_id: int, amount: int, db) -> cart_model:
    from services.Product import get_product

    product = get_product(product_id, db)

    cart = get_cart(user, db)

    items = json.loads(cart.items)

    if str(product_id) in list(items.keys()):
        items[str(product_id)] += amount
    else:
        items[str(product_id)] = amount

    if items[str(product_id)] == 0:
        del items[str(product_id)]

    items = json.dumps(items)
    cart.items = items

    cart.total_price += product.price * amount

    db.commit()
    db.refresh(cart)

    return cart


def remove_item(user: user_dto, product_id: int, amount: int, db):
    from services.Product import get_product

    product = get_product(product_id, db)

    cart = get_cart(user, db)

    items = json.loads(cart.items)
    if str(product_id) in list(items.keys()):
        items[str(product_id)] -= amount
        if items[str(product_id)] == 0:
            del items[str(product_id)]
        elif items[str(product_id)] < 0:
            raise HTTPException(status_code=400, detail="No such amount of available products in your cart")

        items = json.dumps(items)

        cart.items = items

        cart.total_price -= product.price * amount

        if cart.total_price < 0:
            cart.total_price = 0

        db.commit()
        db.refresh(cart)
        return cart

    # Product is not in the user's cart
    raise HTTPException(status_code=400, detail="Invalid product id provided")
