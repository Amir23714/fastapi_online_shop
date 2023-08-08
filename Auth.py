import datetime
import uuid
from datetime import timedelta

import fastapi.security
import jwt
from fastapi import HTTPException
from jose import JWTError
from jwt import ExpiredSignatureError
from passlib.context import CryptContext

import settings
from DTO import User as UserDTO
from services import User as UserServices

class AuthHandler():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hashed_password(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, initial_password, hashed_password):
        return self.pwd_context.verify(initial_password, hashed_password)

    def get_token(self, user: UserDTO.User):
        data = {"sub": user.email, "isAdmin": user.isAdmin}

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
        now = datetime.datetime.now()

        token_expires = now + access_token_expires

        data["exp"] = int(token_expires.timestamp())

        encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt, data["exp"]

    def decode_token(self, token: str, db):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

            return payload

        except ExpiredSignatureError:
            custom_options = {
                "verify_exp": False,
            }
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM,
                                 options=custom_options)

            UserServices.make_user_unlogged_in(UserServices.get_user(payload.get("sub"), db), db)
            db.commit()

            raise HTTPException(status_code=401, detail="Your token has been expired")

    def authentificate_admin(self, access_token, db):
        from services import User as UserServices

        payload = self.decode_token(access_token, db)

        email = payload.get("sub")
        isAdmin = payload.get("isAdmin")
        exp = payload.get("exp")

        user = UserServices.get_user(email, db)

        if not user.isAdmin or user.isAdmin != isAdmin:
            raise HTTPException(status_code=403, detail="You do not have access to browse this page")

        return user

    def authentificate_user(self, access_token, db):
        from services import User as UserServices

        payload = self.decode_token(access_token, db)

        email = payload.get("sub")
        isAdmin = payload.get("isAdmin")
        exp = payload.get("exp")

        user = UserServices.get_user(email, db)

        if user is None:
            raise HTTPException(status_code=400, detail="Invalid email. Valid token. Hmmmm...")

        return user

    def get_apikeyHeader(self, autoerror=True):
        return fastapi.security.APIKeyHeader(name="Authorization", auto_error=autoerror)
