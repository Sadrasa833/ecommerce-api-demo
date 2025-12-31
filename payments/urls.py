from django.urls import path
from .views import CreatePaymentIntentView, PaymentCallbackView

urlpatterns = [
    path("intent/", CreatePaymentIntentView.as_view()),
    path("callback/", PaymentCallbackView.as_view()),
]
