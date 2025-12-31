from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, StartPaymentView, MyOrdersView

router = DefaultRouter()
router.register('', OrderViewSet, basename='order')

urlpatterns = [
    path('payments/start/', StartPaymentView.as_view(), name='start-payment'),
    
    path('mine/', MyOrdersView.as_view(), name='my-orders'),
    
    path('', include(router.urls)),
]