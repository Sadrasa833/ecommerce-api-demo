import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from orders.models import Order


class IdempotencyKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "key"], name="uniq_idempotency_user_key")
        ]


class PaymentIntent(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        SUCCEEDED = "SUCCEEDED", "SUCCEEDED"
        FAILED = "FAILED", "FAILED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment_intent")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    succeeded_at = models.DateTimeField(null=True, blank=True)
