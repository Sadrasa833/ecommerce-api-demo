from django.db.models.signals import post_save
from django.dispatch import receiver

from catalog.models import Product
from .models import StockItem


@receiver(post_save, sender=Product)
def ensure_stock_item(sender, instance: Product, created: bool, **kwargs):
    if created:
        StockItem.objects.get_or_create(product=instance)
