from pydantic import BaseModel

class ResetPassword(BaseModel):
    email: str
    old_password: str
    new_password: str
