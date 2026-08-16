from django.db import models


class NotificationType(models.TextChoices):
    DROP_ALERT = "drop_alert", "Drop Alert"
