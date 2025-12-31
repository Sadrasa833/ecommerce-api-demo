from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.models import InventoryReservation, StockItem, StockMovement
from orders.models import Order
from .models import IdempotencyKey, PaymentIntent
from .serializers import CreateIntentSerializer, CallbackSerializer


class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        idem_key = request.headers.get("Idempotency-Key")
        if not idem_key:
            return Response({"detail": "Idempotency-Key header is required."}, status=400)

        ser = CreateIntentSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        order = get_object_or_404(Order, id=ser.validated_data["order_id"], user=request.user)

        existed = IdempotencyKey.objects.filter(user=request.user, key=idem_key).exists()
        if existed:
            intent = PaymentIntent.objects.filter(order=order).first()
            if intent:
                return Response({"intent_id": str(intent.id), "status": intent.status, "amount": intent.amount}, status=200)

        IdempotencyKey.objects.create(user=request.user, key=idem_key)

        intent, created = PaymentIntent.objects.get_or_create(
            order=order,
            defaults={"amount": order.payable_total},
        )
        return Response({"intent_id": str(intent.id), "status": intent.status, "amount": intent.amount}, status=201)


class PaymentCallbackView(APIView):
    """
    شبیه webhook درگاه.
    """
    @transaction.atomic
    def post(self, request):
        ser = CallbackSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        intent = get_object_or_404(PaymentIntent.objects.select_related("order"), id=ser.validated_data["intent_id"])

        # idempotent callback
        if intent.status == PaymentIntent.Status.SUCCEEDED:
            return Response({"detail": "Already succeeded."}, status=200)

        order = intent.order

        if ser.validated_data["success"] is True:
            # commit inventory reservation
            reservations = list(InventoryReservation.objects.select_for_update().filter(order_id=order.id, consumed_at__isnull=True, released_at__isnull=True))

            # lock stock items
            product_ids = [r.product_id for r in reservations]
            stock_items = list(StockItem.objects.select_for_update().filter(product_id__in=product_ids))
            stock_by_pid = {s.product_id: s for s in stock_items}

            for r in reservations:
                stock = stock_by_pid[r.product_id]
                # reserved -> consume
                stock.reserved -= r.qty
                stock.on_hand -= r.qty
                stock.save(update_fields=["reserved", "on_hand"])

                StockMovement.objects.create(
                    stock_item=stock,
                    type=StockMovement.Type.OUT,
                    qty=r.qty,
                    reason=f"Order {order.id} paid",
                )

                r.consumed_at = timezone.now()
                r.save(update_fields=["consumed_at"])

            order.status = Order.Status.PAID
            order.save(update_fields=["status"])

            intent.status = PaymentIntent.Status.SUCCEEDED
            intent.succeeded_at = timezone.now()
            intent.save(update_fields=["status", "succeeded_at"])

            return Response({"detail": "Payment succeeded."}, status=200)

        # failed
        intent.status = PaymentIntent.Status.FAILED
        intent.save(update_fields=["status"])
        return Response({"detail": "Payment failed."}, status=200)
