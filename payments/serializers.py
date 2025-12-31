from rest_framework import serializers


class CreateIntentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()


class CallbackSerializer(serializers.Serializer):
    intent_id = serializers.UUIDField()
    success = serializers.BooleanField()
