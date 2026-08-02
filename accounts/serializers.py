from typing import ClassVar

from rest_framework import serializers

from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields: ClassVar[list] = ["email", "password", "first_name", "middle_name", "last_name", "phone_number"]
        extra_kwargs: ClassVar[dict] = {
            "middle_name": {"required": False},
            "phone_number": {"required": False},
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
