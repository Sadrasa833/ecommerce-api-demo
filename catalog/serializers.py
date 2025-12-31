from rest_framework import serializers
from .models import Product, Category, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'text', 'created_at']
        read_only_fields = ['user_name', 'created_at']

    def get_user_name(self, obj):
        if hasattr(obj.user, 'full_name') and obj.user.full_name:
            return obj.user.full_name
        return obj.user.phone_number

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            "id", 
            "name", 
            "sku", 
            "description", 
            "price", 
            "is_active", 
            "category", 
            "image"
        ]