import pytest
import requests
from math import ceil

def test_health_check(app_url):
    response = requests.get(f"{app_url}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_status_check(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_user_data(app_url):
    response = requests.get(f"{app_url}/api/users?page=2&size=6")
    assert response.status_code == 200

    users = response.json()["items"]
    assert len(users) > 0

    user_data = users[0]
    assert user_data["id"] == 7
    assert user_data["email"] == "michael.lawson@reqres.in"

def test_invalid_user(app_url):
    response = requests.get(f"{app_url}/api/users/23")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

@pytest.mark.parametrize("page_size", [1, 3, 5, 6, 10])
def test_users_pagination_structure(app_url, page_size):
    response = requests.get(f"{app_url}/api/users", params={"page": 1, "size": page_size})
    assert response.status_code == 200

    data = response.json()

    total = data["total"]
    items = data["items"]
    pages = data["pages"]
    size = data["size"]
    page = data["page"]

    assert size == page_size
    assert page == 1
    assert len(items) <= page_size
    assert pages == ceil(total / page_size)

@pytest.mark.parametrize("page_size", [2, 4, 5])
def test_total_pages_dynamic(app_url, page_size):
    response = requests.get(f"{app_url}/api/users", params={"size": page_size})
    assert response.status_code == 200

    data = response.json()
    total = data["total"]
    expected_pages = ceil(total / page_size)

    assert data["pages"] == expected_pages

def test_different_data_on_different_pages(app_url):
    page_size = 5
    response_page_1 = requests.get(f"{app_url}/api/users", params={"page": 1, "size": page_size})
    response_page_2 = requests.get(f"{app_url}/api/users", params={"page": 2, "size": page_size})

    assert response_page_1.status_code == 200
    assert response_page_2.status_code == 200

    data_page_1 = response_page_1.json()["items"]
    data_page_2 = response_page_2.json()["items"]

    ids_page_1 = {user["id"] for user in data_page_1}
    ids_page_2 = {user["id"] for user in data_page_2}

    assert ids_page_1.isdisjoint(ids_page_2)

def test_create_user(app_url):
    payload = {"name": "stefano", "job": "tester"}
    response = requests.post(f"{app_url}/api/users", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert "id" in body
    assert "createdAt" in body

def test_update_user(app_url):
    payload = {"name": "stefano", "job": "zion resident"}
    response = requests.put(f"{app_url}/api/users/2", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert "updatedAt" in body

def test_delete_user(app_url):
    response = requests.delete(f"{app_url}/api/users/2")
    assert response.status_code == 204
    assert response.text == ""

def test_success_register(app_url):
    payload = {"email": "eve.holt@reqres.in", "password": "password"}
    response = requests.post(f"{app_url}/api/register", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert "id" in body
    assert "token" in body

@pytest.mark.parametrize("page,size", [(1, 3), (2, 3), (3, 3)])
def test_paginated_users_expected_items_count(app_url, page, size):
    response = requests.get(f"{app_url}/api/users", params={"page": page, "size": size})

    if response.status_code == 404:
        data = response.json()
        assert data["detail"] == "Page not found"
        return

    data = response.json()
    total = data["total"]
    pages = data["pages"]

    expected_pages = ceil(total / size)
    assert pages == expected_pages
    assert data["size"] == size
    assert data["page"] == page

    if page < pages:
        assert len(data["items"]) == size
    else:
        assert len(data["items"]) <= size