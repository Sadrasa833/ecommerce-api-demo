from django.db import models
from django.conf import settings 

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", null=True, blank=True)
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=64, unique=True)  
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()  
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True) #

    def __str__(self):
        return f"{self.user} on {self.product}"
