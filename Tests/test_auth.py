import json
from typing import List

import pytest

from conftest import client


user_token = None
admin_token = None

@pytest.fixture
def test_users():
    user = {"name": "Karim", "email": "karim@mail.ru", "password": "Karim2014", "isLoggedIn": False, "isAdmin": False}
    admin = {"name": "Amir", "email": "amir@mail.ru", "password": "Amir2004", "isLoggedIn": False, "isAdmin": True}
    return [admin, user]

@pytest.fixture
def test_products():
    shampoo = {"name" : "Shampoo", "amount" : 10, "description" : "Shampoo for hair", "price" : 1000, "isVisible" : True}
    shower_gel = {"name" : "Shower gel", "amount" : 1, "description" : "Shower gel for body", "price" : 500, "isVisible" : False}
    return [shampoo, shower_gel]



class TestUserProfile:

    def test_register(self, test_users):
        response = client.post("api/profile/register", json=test_users[1])
        assert response.status_code == 201
        response = client.post("api/profile/register", json = test_users[0])
        assert response.status_code == 201

    def test_login(self, test_users):
        global user_token, admin_token

        response = client.post("api/profile/login", json=test_users[1])
        assert response.status_code == 201
        user_token = response.json()["access_token"]

        response = client.post("api/profile/login", json=test_users[0])
        assert response.status_code == 201
        admin_token = response.json()["access_token"]

    def test_relogin(self):
        pass

class TestProduct:

    def test_get(self):
        response = client.get("api/products")
        data = json.loads(response.text)
        assert len(data) == 0

    def test_add(self, test_products):
        global admin_token
        response = client.post("api/products", json = test_products[0], headers={"Authorization" : admin_token})
        assert response.json() == test_products[0]

        response = client.post("api/products", json=test_products[1], headers={"Authorization": admin_token})
        assert response.json() == test_products[1]


    def test_get_2(self):
        global admin_token, user_token
        response = client.get("api/products", headers={"Authorization": user_token})
        data = json.loads(response.text)
        assert len(data) == 1

        response = client.get("api/products", headers={"Authorization": admin_token})
        data = json.loads(response.text)
        assert len(data) == 2

    def test_remove(self):
        response = client.delete("api/products", params= {"id" : 1}, headers={"Authorization" : admin_token})
        assert response.status_code == 201

    def test_get_3(self):
        response = client.get("api/products")
        data = json.loads(response.text)
        assert len(data) == 0

    def test_change(self):
        response = client.put("api/products", json = {"id" : 2, "isVisible" : True}, headers={"Authorization": admin_token})
        assert response.status_code == 201

    def test_get_4(self):
        response = client.get("api/products")
        data = json.loads(response.text)
        assert len(data) == 1

class TestUserCart:

    def test_get(self):
        global user_token
        response = client.get("api/profile/cart", headers={"Authorization": user_token} )
        assert response.status_code == 200

    def test_post(self):
        global user_token
        response = client.post("api/profile/cart",json = {"id" : 2, "amount" : 1}, headers={"Authorization": user_token})
        items = json.loads(response.json()["items"])
        assert items["2"] == 1

        response = client.post("api/profile/cart", json={"id": 2, "amount": 1}, headers={"Authorization": user_token})
        assert response.status_code == 400

    def test_remove(self):
        global user_token
        response = client.delete("api/profile/cart", params={"id": 2, "amount": 1}, headers={"Authorization": user_token})
        assert response.status_code == 201

        response = client.delete("api/profile/cart", params={"id": 2, "amount": 1}, headers={"Authorization": user_token})
        assert response.status_code == 400



