from django.urls import path
from .views import OTPRequestView, OTPVerifyView, MeView,ProfileUpdateView

urlpatterns = [
    path("otp/request/", OTPRequestView.as_view(), name="otp-request"),
    path("otp/verify/", OTPVerifyView.as_view(), name="otp-verify"),
    path("me/", MeView.as_view(), name="user-profile"),
     path("me/update/", ProfileUpdateView.as_view(), name='user-update'),  # 👈
]
