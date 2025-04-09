from http.client import responses

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'somewierdemail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''

    new_unique_client = {
        "name": 'Semen Semenov',
        "email": 'newclient.com'
    }

    response = client.post("/api/v1/user", json=new_unique_client)
    assert response.status_code == 201
    new_clent_id = response.json()
    assert isinstance(new_clent_id, int)

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    response = client.post("/api/v1/user", json={ "name": users[0]["name"],
                                                      "email": users[0]["email"]})
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    response = client.get("/api/v1/user", params={'email': users[1]['email']})
    assert response.status_code == 200
    response = client.delete("/api/v1/user", params={'email': users[1]['email']})
    assert response.status_code == 204
    response = client.get("/api/v1/user", params={'email': users[1]['email']})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
