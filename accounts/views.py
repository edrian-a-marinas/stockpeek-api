from typing import ClassVar

from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer
from .services import login_user, register_user


class RegisterView(APIView):
    permission_classes: ClassVar[list] = []

    @method_decorator(ratelimit(key="ip", rate="10/m", block=True))
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = register_user(serializer.validated_data, request)
        return Response({"email": user.email, "first_name": user.first_name}, status=201)


class LoginView(APIView):
    permission_classes: ClassVar[list] = []

    @method_decorator(ratelimit(key="ip", rate="5/m", block=True))
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = login_user(serializer.validated_data, request)
        login(request, user)
        return Response({"email": user.email, "first_name": user.first_name}, status=200)
