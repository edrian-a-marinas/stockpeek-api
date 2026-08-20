import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_register_success(client):
    payload = {
        "email": "new@stockpeek.com",
        "password": "testpass123",
        "first_name": "New",
        "last_name": "User",
    }
    response = client.post(reverse("register"), payload)
    assert response.status_code == 201
    assert response.data["email"] == "new@stockpeek.com"


def test_register_duplicate_email(client, existing_user):
    payload = {
        "email": existing_user.email,
        "password": "testpass123",
        "first_name": "Dup",
        "last_name": "User",
    }
    response = client.post(reverse("register"), payload)
    assert response.status_code == 400


def test_login_success(client, existing_user):
    payload = {"email": existing_user.email, "password": "testpass123"}
    response = client.post(reverse("login"), payload)
    assert response.status_code == 200
    assert response.data["email"] == existing_user.email


def test_login_invalid_credentials(client, existing_user):
    payload = {"email": existing_user.email, "password": "wrongpass"}
    response = client.post(reverse("login"), payload)
    assert response.status_code == 403


def test_logout_success(client, existing_user):
    payload = {"email": existing_user.email, "password": "testpass123"}
    client.post(reverse("login"), payload)
    response = client.post(reverse("logout"))
    assert response.status_code == 204
