from rest_framework import serializers


class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)  # Validating basic input


class VerifyPaymentSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()
