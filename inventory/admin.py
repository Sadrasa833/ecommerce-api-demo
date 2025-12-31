from django.contrib import admin
from .models import StockItem, StockMovement, InventoryReservation


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "on_hand", "reserved", "available")
    search_fields = ("product__name", "product__sku")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("id", "stock_item", "type", "qty", "reason", "created_at")
    list_filter = ("type", "created_at")


@admin.register(InventoryReservation)
class InventoryReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "product", "qty", "expires_at", "consumed_at", "released_at", "created_at")
    search_fields = ("order_id", "product__sku")
