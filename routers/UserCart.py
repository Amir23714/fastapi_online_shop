from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.models import get_db

from DTO.ProductServer import ProductServer as productserver_dto
from DTO.UserCart import UserCart as usercart_dto
from services import UserCart as CartServices, Product as ProductServices

from Auth import AuthHandler

auth = AuthHandler()
router = APIRouter()


@router.post("", status_code=201)
async def add_item(data: productserver_dto, access_token: Annotated[str, Depends(auth.get_apikeyHeader())],
                   db: Session = Depends(get_db)):
    """This endpoint is used to add item to user's cart"""
    user = auth.authentificate_user(access_token,db)

    product = ProductServices.get_product(data.id, db)

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount of products must be positive")

    if product.amount >= data.amount and product.isVisible:
        try:
            product = ProductServices.update_amount(data.id, product.amount - data.amount, db)
            cart = CartServices.add_item(user, data.id, data.amount, db)

            db.commit()
            db.refresh(cart)
            return cart

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    raise HTTPException(status_code=400, detail="No such amount of available products")


@router.delete("", status_code=201)
async def remove_item(id : int, amount : int, access_token: Annotated[str, Depends(auth.get_apikeyHeader())],
                      db: Session = Depends(get_db)):
    """This endpoint is used to remove item from user's cart"""
    user = auth.authentificate_user(access_token,db)

    product = ProductServices.get_product(id, db)

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount of products must be positive")

    try:
        cart = CartServices.remove_item(user, id, amount, db)

        ProductServices.update_amount(id, product.amount + amount, db)

        db.commit()
        db.refresh(cart)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return cart


@router.get("", status_code=200)
async def get_cart(access_token: Annotated[str, Depends(auth.get_apikeyHeader())], db: Session = Depends(get_db)):
    """This endpoint is used to get user's cart"""
    user = auth.authentificate_user(access_token,db)
    return CartServices.get_cart(user, db)
