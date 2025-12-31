from django.db import transaction
from django.utils import timezone
from celery import shared_task

from .models import InventoryReservation, StockItem


@shared_task
def release_expired_reservations(batch_size: int = 200) -> int:
    now = timezone.now()

    with transaction.atomic():
        expired = list(
            InventoryReservation.objects.select_for_update(skip_locked=True)
            .filter(expires_at__lt=now, consumed_at__isnull=True, released_at__isnull=True)
            .order_by("expires_at")[:batch_size]
        )

        if not expired:
            return 0

        product_ids = [r.product_id for r in expired]
        stock_items = list(StockItem.objects.select_for_update().filter(product_id__in=product_ids))
        stock_by_pid = {s.product_id: s for s in stock_items}

        for r in expired:
            stock = stock_by_pid[r.product_id]
            stock.reserved = max(0, stock.reserved - r.qty)
            stock.save(update_fields=["reserved"])

            r.released_at = now
            r.save(update_fields=["released_at"])

        return len(expired)
