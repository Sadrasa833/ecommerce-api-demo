from django.contrib import admin
from .models import PhoneOTP, UserProfile


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "expires_at", "consumed_at", "attempts", "created_at")
    search_fields = ("phone_number",)
    list_filter = ("created_at",)
    readonly_fields = ("code_hash", "created_at")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone_number", "full_name", "created_at")
    search_fields = ("phone_number", "full_name", "user__username")
