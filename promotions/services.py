from dataclasses import dataclass
from django.db import transaction
from django.utils import timezone

from orders.models import Order
from .models import Coupon, CouponRedemption


@dataclass(frozen=True)
class CouponApplyResult:
    discount_total: int
    payable_total: int


def compute_discount(*, coupon: Coupon, subtotal: int) -> int:
    if subtotal < coupon.min_subtotal:
        return 0

    if coupon.type == Coupon.Type.PERCENT:
        pct = max(0, min(100, int(coupon.value)))
        return (subtotal * pct) // 100

    if coupon.type == Coupon.Type.FIXED:
        return min(subtotal, int(coupon.value))

    return 0


@transaction.atomic
def apply_coupon_to_order(*, user, order: Order, code: str) -> CouponApplyResult:
    coupon = Coupon.objects.select_for_update().filter(code=code).first()
    if not coupon or not coupon.is_valid_now():
        raise ValueError("Invalid coupon.")

    if order.status != Order.Status.PENDING_PAYMENT:
        raise ValueError("Coupon can only be applied to PENDING_PAYMENT orders.")

    if coupon.usage_limit_total is not None:
        used_total = CouponRedemption.objects.filter(coupon=coupon).count()
        if used_total >= coupon.usage_limit_total:
            raise ValueError("Coupon usage limit reached.")

    if coupon.usage_limit_per_user is not None:
        used_user = CouponRedemption.objects.filter(coupon=coupon, user=user).count()
        if used_user >= coupon.usage_limit_per_user:
            raise ValueError("You have reached coupon usage limit.")

    discount = compute_discount(coupon=coupon, subtotal=order.subtotal)
    if discount <= 0:
        raise ValueError("Coupon not applicable for this order.")

    order.discount_total = discount
    order.payable_total = max(0, order.subtotal - discount)
    order.save(update_fields=["discount_total", "payable_total"])

    CouponRedemption.objects.get_or_create(user=user, coupon=coupon, order_id=order.id)

    return CouponApplyResult(discount_total=order.discount_total, payable_total=order.payable_total)
