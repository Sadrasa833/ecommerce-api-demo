from rest_framework import serializers

class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

    def save(self, **kwargs):
        
        code = self.validated_data["code"]
        return {"code": code, "valid": True, "discount_amount": 0}
