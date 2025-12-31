from django.urls import path
from .views import CartView, CartItemAddView, CartItemUpdateDeleteView

urlpatterns = [
    path("", CartView.as_view()),
    path("items/", CartItemAddView.as_view()),
    path("items/<int:item_id>/", CartItemUpdateDeleteView.as_view()),
]
