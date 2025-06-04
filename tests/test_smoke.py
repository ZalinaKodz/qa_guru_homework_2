
import pytest
import requests

def test_health_check(app_url):  # Проверка работоспособности сервиса
    response = requests.get(f"{app_url}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_user_data(app_url): #Проверка данных пользователя

    response = requests.get(f"{app_url}/api/users?page=2")
    print(response.text)
    assert response.status_code == 200
    user_data = response.json()["data"][0]
    expected_id = 7
    expected_email = "michael.lawson@reqres.in"
    assert user_data["id"] == expected_id
    assert user_data["email"] == expected_email


def test_invalid_user(app_url):     # Проверка на несуществующего пользователя

    response = requests.get(f"{app_url}/api/users/23")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_users_count_matches_per_page(app_url):   # Проверка, что количество пользователей соответствует количеству на странице

    response = requests.get(f"{app_url}/api/users?page=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == data["per_page"]

@pytest.mark.parametrize("per_page, expected_pages", [
    (5, 3),  # 12 / 5 = 2.4 => 3 страницы
    (6, 2),  # 12 / 6 = 2 => 2 страницы
    (8, 2),  # 12 / 8 = 1.5 => 2 страницы
    (10, 2),  # 12 / 10 = 1.2 => 2 страницы
])
def test_total_pages_for_different_sizes(app_url, per_page, expected_pages):
    response = requests.get(f"{app_url}/api/users", params={"page": 1, "per_page": per_page})
    assert response.status_code == 200
    body = response.json()
    assert body["total_pages"] == expected_pages

def test_different_data_on_different_pages(app_url):
    response1 = requests.get(f"{app_url}/api/users", params={"page": 1, "per_page": 5})
    response2 = requests.get(f"{app_url}/api/users", params={"page": 2, "per_page": 5})

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()["data"]
    data2 = response2.json()["data"]

    assert data1 != data2
    # Убедимся, что ни один id не повторяется
    ids1 = {user["id"] for user in data1}
    ids2 = {user["id"] for user in data2}
    assert ids1.isdisjoint(ids2)


def test_create_user(app_url):   # Проверка создания пользователя
    payload = {
        "name": "stefano",
        "job": "tester"
    }
    response = requests.post(f"{app_url}/api/users", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert "id" in body
    assert "createdAt" in body


def test_update_user(app_url): # Проверка обновления пользователя
    url = f"{app_url}/api/users/2"
    payload = {
        "name": "stefano",
        "job": "zion resident"
    }
    response = requests.put(url, json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert body["updatedAt"] is not None


def test_delete_user(app_url): # Проверка удаления пользователя
    url = f"{app_url}/api/users/2"
    response = requests.delete(url)
    assert response.status_code == 204
    assert response.text == ""


def test_success_register(app_url): # Проверка успешной регистрации пользователя
    url = f"{app_url}/api/register"
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "password"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "token" in body