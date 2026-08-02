import logging

from django.http import JsonResponse
from django_ratelimit.exceptions import Ratelimited
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("config.limiter")


def custom_exception_handler(exc, context):
    if isinstance(exc, Ratelimited):
        request = context["request"]
        ip = request.META.get("REMOTE_ADDR")
        logger.warning(f"RATELIMIT | path={request.path} | ip={ip} | status=blocked | reason=too many requests")
        return JsonResponse({"detail": "Too many requests. Please try again later."}, status=429)
    return drf_exception_handler(exc, context)
