from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemAddSerializer, CartItemUpdateSerializer


def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = _get_or_create_cart(request.user)
        cart = Cart.objects.filter(id=cart.id).prefetch_related("items__product__category").first()
        return Response(CartSerializer(cart).data, status=200)


class CartItemAddView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        ser = CartItemAddSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        cart = _get_or_create_cart(request.user)
        product = get_object_or_404(Product, id=ser.validated_data["product_id"], is_active=True)
        qty = ser.validated_data["qty"]

        try:
            item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"qty": qty})
            if not created:
                item.qty += qty
                item.save(update_fields=["qty"])
        except IntegrityError:
            return Response({"detail": "Could not add item."}, status=400)

        return Response({"detail": "Added."}, status=201)


class CartItemUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, item_id: int):
        ser = CartItemUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        cart = _get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        item.qty = ser.validated_data["qty"]
        item.save(update_fields=["qty"])
        return Response({"detail": "Updated."}, status=200)

    @transaction.atomic
    def delete(self, request, item_id: int):
        cart = _get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return Response(status=204)
