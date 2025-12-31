from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer
from catalog.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        items_data = request.data.get('items', [])
        
        if not items_data:
            return Response({"detail": "سبد خرید خالی است"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=request.user, 
            status=Order.Status.PENDING_PAYMENT
        )

        total_price = 0

        
        for item in items_data:
            product = get_object_or_404(Product, id=item['product_id'])
            qty = item.get('quantity', 1)
            price = product.price  
            
            line_total = price * qty
            total_price += line_total

            OrderItem.objects.create(
                order=order, 
                product=product, 
                qty=qty, 
                unit_price=price,
                line_total=line_total
            )

      
        order.subtotal = total_price
        order.payable_total = total_price
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class StartPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        gateway = request.data.get('gateway', 'zarinpal')
        
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        amount = order.payable_total

        Payment.objects.create(order=order, gateway=gateway, amount=amount)

        return Response({
            'url': 'https://google.com', 
            'message': 'لینک پرداخت ساخته شد'
        })