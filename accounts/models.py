from django.conf import settings
from django.db import models
from django.utils import timezone


class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=20, db_index=True)
    code_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    

    def is_valid(self) -> bool:
        return self.consumed_at is None and timezone.now() < self.expires_at

def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.user_id}/{filename}"


class UserProfile(models.Model):
   
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    national_id = models.CharField(max_length=10, blank=True)
    avatar = models.ImageField(
        upload_to=user_avatar_path, blank=True, null=True
    ) 

    def __str__(self) -> str:
        return self.phone_number
