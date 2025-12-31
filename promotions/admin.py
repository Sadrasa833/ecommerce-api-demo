from django.contrib import admin
from .models import Coupon, CouponRedemption


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "type", "value", "min_subtotal", "is_active", "starts_at", "ends_at")
    search_fields = ("code",)
    list_filter = ("type", "is_active")


@admin.register(CouponRedemption)
class CouponRedemptionAdmin(admin.ModelAdmin):
    list_display = ("id", "coupon", "user", "order_id", "created_at")
    search_fields = ("coupon__code", "user__username", "order_id")
