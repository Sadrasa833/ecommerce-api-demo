from django.db import models
from django.utils import timezone
from catalog.models import Product


class StockItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="stock")
    on_hand = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)

    @property
    def available(self) -> int:
        return int(self.on_hand) - int(self.reserved)

    def __str__(self) -> str:
        return f"{self.product.sku} on_hand={self.on_hand} reserved={self.reserved}"


class StockMovement(models.Model):
    class Type(models.TextChoices):
        IN = "IN", "IN"
        OUT = "OUT", "OUT"
        ADJUST = "ADJUST", "ADJUST"

    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name="movements")
    type = models.CharField(max_length=10, choices=Type.choices)
    qty = models.IntegerField()  
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class InventoryReservation(models.Model):
    
    order_id = models.BigIntegerField(db_index=True) 
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["order_id", "created_at"]),
        ]

    @property
    def is_active(self) -> bool:
        return self.consumed_at is None and self.released_at is None and timezone.now() < self.expires_at
