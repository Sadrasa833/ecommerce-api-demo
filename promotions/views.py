# promotions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Coupon

class ApplyCouponView(APIView):
    def post(self, request):
        code = request.data.get("code")
        total_price = request.data.get("total_price", 0) # دریافت مبلغ کل از فرانت
        
        try:
            coupon = Coupon.objects.get(code=code)
            
            # بررسی اعتبار زمانی
            if not coupon.is_valid_now():
                return Response({"detail": "کد تخفیف منقضی شده است ⏳"}, status=400)

            # --- محاسبه مبلغ تخفیف ---
            final_discount = 0

            # 1. اگر درصدی بود
            if coupon.type == Coupon.Type.PERCENT:
                # فرمول: (مبلغ کل * درصد) تقسیم بر 100
                final_discount = (int(total_price) * coupon.value) // 100
            
            # 2. اگر مبلغ ثابت بود
            else: # Coupon.Type.FIXED
                final_discount = coupon.value

            # جلوگیری از اینکه تخفیف بیشتر از کل قیمت شود
            if final_discount > int(total_price):
                final_discount = int(total_price)

            return Response({
                "code": coupon.code,
                "amount": final_discount, # مبلغ نهایی محاسبه شده (به تومان)
                "type": coupon.type,
                "message": "تخفیف اعمال شد ✅"
            })
            
        except Coupon.DoesNotExist:
            return Response({"detail": "کد تخفیف وجود ندارد ❌"}, status=400)