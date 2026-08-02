import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from accounts.models import User
from config.cache import get_cache, set_cache

logger = logging.getLogger(__name__)

CACHE_TTL_AUTH = settings.CACHE_TTL_AUTH  # 30 days


def register_user(validated_data, request):
    ip = request.META.get("REMOTE_ADDR")
    try:
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            middle_name=validated_data.get("middle_name"),
            last_name=validated_data["last_name"],
            phone_number=validated_data.get("phone_number"),
        )
        logger.info(f"REGISTER | email={user.email} | ip={ip} | status=success")
        return user
    except IntegrityError:
        logger.warning(f"REGISTER | email={validated_data['email']} | ip={ip} | status=failed | reason=email already exists")
        raise ValidationError("Email already exists.")


def login_user(validated_data, request):
    ip = request.META.get("REMOTE_ADDR")
    user = authenticate(email=validated_data["email"], password=validated_data["password"])
    if user is None:
        logger.warning(f"LOGIN | email={validated_data['email']} | ip={ip} | status=failed | reason=invalid credentials")
        raise AuthenticationFailed("Invalid email or password.")

    cache_key = f"user:{user.id}"
    cached_user = get_cache(cache_key)
    if cached_user is None:
        set_cache(cache_key, {"email": user.email, "first_name": user.first_name}, CACHE_TTL_AUTH)
        source = "database"
    else:
        source = "cache"

    logger.info(f"LOGIN | email={user.email} | ip={ip} | source={source} | status=success")
    return user


def logout_user(request):
    ip = request.META.get("REMOTE_ADDR")
    email = request.user.email
    logger.info(f"LOGOUT | email={email} | ip={ip} | status=success")
