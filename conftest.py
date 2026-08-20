import pytest
from django.conf import settings
from rest_framework.test import APIClient

from accounts.models import User

settings.RATELIMIT_ENABLED = False


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def existing_user():
    return User.objects.create_user(
        email="seed@stockpeek.com",
        password="testpass123",
        first_name="Seed",
        last_name="User",
    )


@pytest.fixture
def authenticated_client(client, existing_user):
    client.force_authenticate(user=existing_user)
    return client
