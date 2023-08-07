from models.models import User as user_model
from sqlalchemy.orm import Session
from DTO.User import User as user_dto


def create_user(data: user_dto, db):
    user = user_model(name=data.name, email=data.email, password=data.password, isAdmin=data.isAdmin)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except Exception as e:
        print(e)

    return user


def get_user(email: str, db):
    return db.query(user_model).filter(user_model.email == email).first()


def make_user_logged_in(user: user_model, db):
    user.isLoggedIn = True
    db.commit()
    db.refresh(user)
    return user

def make_user_unlogged_in(user: user_model, db):
    user.isLoggedIn = False
    db.commit()
    db.refresh(user)
    return user


def change_password(user: user_model, new_password: str, db):
    user.password = new_password
    db.commit()
    db.refresh(user)
    return user
