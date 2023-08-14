from typing import Annotated, List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.models import get_db

from DTO.Product import Product as product_dto
from DTO.ProductUpdate import ProductUpdate as productupdate_dto

from services import User as UserServices
from services import Product as ProductServices
from Auth import AuthHandler

auth = AuthHandler()
router = APIRouter()


@router.get("", status_code=200, response_model=List[product_dto])
async def get_list_of_products(access_token: Annotated[str, Depends(auth.get_apikeyHeader(autoerror=False))],
                               db: Session = Depends(get_db)):
    """This endpoint is used to get list of all(including unavailable ones for admins) products."""
    if access_token:
        payload = auth.decode_token(access_token, db)

        email = payload.get("sub")
        isAdmin = payload.get("isAdmin")

        user = UserServices.get_user(email, db)

        if user.isAdmin != isAdmin:
            raise HTTPException(status_code=400, detail="Wrong credentials")

        if user.isAdmin:
            return ProductServices.get_all_products(db)

    return ProductServices.get_products(db)


@router.post("", status_code=201, response_model=product_dto)
async def add_product(data: product_dto, access_token: Annotated[str, Depends(auth.get_apikeyHeader())],
                      db: Session = Depends(get_db)):
    """This endpoint is used to add product to the product list (only for admins)"""
    user = auth.authentificate_admin(access_token, db)
    try:
        product = ProductServices.create_product(data, db)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return product


@router.delete("", status_code=201, response_model=Dict)
async def remove_product(id : int, access_token: Annotated[str, Depends(auth.get_apikeyHeader())],
                         db: Session = Depends(get_db)):
    """This endpoint is used to remove product from the product list (only for admins)"""
    user = auth.authentificate_admin(access_token, db)

    try:
        ProductServices.delete_product(id, db)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"status" : "OK"}


@router.put("", status_code=201, response_model=product_dto)
async def change_product(data: productupdate_dto, access_token: Annotated[str, Depends(auth.get_apikeyHeader())],
                         db: Session = Depends(get_db)):
    """This endpoint is used to make changes in product description"""
    user = auth.authentificate_admin(access_token, db)

    product = None
    try:
        if data.amount:
            product = ProductServices.update_amount(data.id, data.amount, db)
        if data.price:
            product = ProductServices.update_price(data.id, data.price, db)
        if data.description:
            product = ProductServices.update_description(data.id, data.description, db)
        if data.isVisible:
            product = ProductServices.update_visibility(data.id, data.isVisible, db)
        if product is None:
            return ProductServices.get_product(data.id, db)

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return product
