from django.conf import settings
from django.db import models
from django.utils import timezone
from catalog.models import Product

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING_PAYMENT = "PENDING_PAYMENT", "PENDING_PAYMENT"
        PAID = "PAID", "PAID"
        CANCELLED = "CANCELLED", "CANCELLED"
        SENT = "SENT", "SENT"  

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_PAYMENT)
    
    
    subtotal = models.PositiveIntegerField(default=0)
    discount_total = models.PositiveIntegerField(default=0)
    payable_total = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Order {self.id} ({self.user})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    line_total = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.qty} x {self.product}"



class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    gateway = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()     
    is_successful = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"