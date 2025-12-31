from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=10)


class MeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    phone_number = serializers.CharField(allow_null=True, allow_blank=True)
    full_name = serializers.CharField(allow_null=True, allow_blank=True)
    national_id = serializers.CharField(
        allow_null=True, allow_blank=True, required=False
    )
    email = serializers.EmailField(
        allow_null=True, allow_blank=True, required=False
    )
    avatar_url = serializers.CharField(
        allow_null=True, allow_blank=True, required=False
    )  


class ProfileUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(allow_blank=True, required=False)
    phone_number = serializers.CharField(allow_blank=True, required=False)
    national_id = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    avatar = serializers.ImageField(required=False, allow_null=True)

class RequestOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'first_name', 'last_name', 'email']

    def get_phone_number(self, obj):
        if hasattr(obj, 'phone_number'):
            return obj.phone_number
        return obj.username 

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']