
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RequestOTPSerializer, VerifyOTPSerializer, UserSerializer, UpdateUserSerializer

User = get_user_model()


otp_storage = {}

class OTPRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            
            
            code = "12345"
            otp_storage[phone] = code
            
            print(f"📩 OTP Generated for {phone}: {code}")
            return Response({"message": "کد ارسال شد", "code": code})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print("📥 Verify Request Data:", request.data)

        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        
        stored_code = otp_storage.get(phone)

        if stored_code and stored_code == code:
            
            user, created = User.objects.get_or_create(username=phone)
            
            if created:
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)
            
            del otp_storage[phone]

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_new_user': created
            })
        
        print("❌ Code Mismatch")
        return Response({"detail": "کد اشتباه یا منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request):
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)