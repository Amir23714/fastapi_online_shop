from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name:str
    email : EmailStr
    password : str
    isLoggedIn : bool = False
    isAdmin : bool = False