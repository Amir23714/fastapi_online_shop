from pydantic import BaseModel


class TokenResponseModel(BaseModel):
    status : str = "OK"
    access_token : str
    exp : int
    token_type :str = "bearer"
