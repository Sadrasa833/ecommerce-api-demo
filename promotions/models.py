from django.conf import settings
from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    class Type(models.TextChoices):
        PERCENT = "PERCENT", "Percent"
        FIXED = "FIXED", "Fixed"

    code = models.CharField(max_length=40, unique=True)
    type = models.CharField(max_length=10, choices=Type.choices)
    value = models.PositiveIntegerField()  
    min_subtotal = models.PositiveIntegerField(default=0)

    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    usage_limit_total = models.PositiveIntegerField(null=True, blank=True)   
    usage_limit_per_user = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid_now(self) -> bool:
        now = timezone.now()
        if not self.is_active:
            return False
        if self.starts_at and now < self.starts_at:
            return False
        if self.ends_at and now > self.ends_at:
            return False
        return True

    def __str__(self) -> str:
        return self.code


class CouponRedemption(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="redemptions")
    order_id = models.BigIntegerField(db_index=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [models.Index(fields=["coupon", "created_at"])]
        constraints = [
            models.UniqueConstraint(fields=["coupon", "order_id"], name="uniq_coupon_order"),
        ]
