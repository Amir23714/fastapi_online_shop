# sddsa
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.models import get_db

from DTO import User as UserDTO
from DTO.ResetPassword import ResetPassword
from DTO.TokenResponseModel import TokenResponseModel

from services import User as UserServices
from services import UserCart as CartServices
from services import Token as TokenServices

from Auth import AuthHandler

auth = AuthHandler()

router = APIRouter()


@router.post("/register", response_model=UserDTO.User, status_code=201)
async def register(data: UserDTO.User = None, db: Session = Depends(get_db)):
    if UserServices.get_user(data.email, db) is not None:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_password = auth.get_hashed_password(data.password)
    data.password = hashed_password

    try:
        user = UserServices.create_user(data, db)
        CartServices.create_cart(user, db)

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return user


@router.post("/login", status_code=201, response_model=TokenResponseModel)
async def login(data: UserDTO.User = None, db: Session = Depends(get_db)):
    user = UserServices.get_user(data.email, db)

    if user is None or not auth.verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="User with this email and/or password does not exist")

    if user.isLoggedIn:
        raise HTTPException(status_code=400, detail="You are already logged in")

    # Building a transaction. Each commit will be rolled back if error occurs
    try:
        user = UserServices.make_user_logged_in(user, db)
        token, exp = auth.get_token(user)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "OK", "access_token": token, "exp": exp, "token_type": "bearer"}


@router.post("/resetpassword", status_code=201, response_model=TokenResponseModel)
async def reset(data: ResetPassword, db: Session = Depends(get_db)):
    """This method is used to reset user's password.
    If credentials are invalid, exceptions are raised"""

    user = UserServices.get_user(data.email, db)

    if user is None or not auth.verify_password(data.old_password, user.password):
        raise HTTPException(status_code=400, detail="User with this email and/or password does not exist")

    try:
        user = UserServices.change_password(user, auth.get_hashed_password(data.new_password), db)

        user = UserServices.make_user_logged_in(user, db)


    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    token, exp = auth.get_token(user)

    return {"status": "OK", "access_token": token, "exp": exp, "token_type": "bearer"}


@router.get("", status_code=201, response_model=UserDTO.User)
async def get_user_info(access_token: Annotated[str, Depends(auth.get_apikeyHeader())], db: Session = Depends(get_db)):
    user = auth.authentificate_user(access_token, db)

    return user
