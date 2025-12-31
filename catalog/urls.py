from django.urls import path
from .views import ProductViewSet, CategoryViewSet, ReviewViewSet

urlpatterns = [
    path('categories/', CategoryViewSet.as_view({'get': 'list'}), name='category-list'),

    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),

    path('products/<int:product_pk>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-reviews'),
]