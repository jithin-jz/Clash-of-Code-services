import razorpay
from django.conf import settings
from django.db import transaction
from rest_framework import views, status, permissions
from rest_framework.response import Response

from xpoint.services import XPService
from .models import Payment
from .serializers import CreateOrderSerializer, VerifyPaymentSerializer

# Initialize Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateOrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount_inr = serializer.validated_data["amount"]

        # Amount in Paise
        data = {
            "amount": amount_inr * 100,
            "currency": "INR",
            "notes": {"user_id": request.user.id},
        }

        try:
            order = client.order.create(data=data)

            XP_PACKAGES_MAP = {
                49: 50,
                99: 100,
                199: 200,
                249: 250,
                499: 500,
                749: 800,
                999: 1000,
                1999: 2500,
            }

            if amount_inr not in XP_PACKAGES_MAP:
                return Response(
                    {"error": "Invalid package amount"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            xp_to_credit = XP_PACKAGES_MAP[amount_inr]

            Payment.objects.create(
                user=request.user,
                razorpay_order_id=order["id"],
                amount=amount_inr,
                xp_amount=xp_to_credit,
                status="pending",
            )

            return Response(
                {
                    "order_id": order["id"],
                    "amount": data["amount"],
                    "key": settings.RAZORPAY_KEY_ID,
                    "xp_amount": xp_to_credit,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VerifyPaymentSerializer

    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": data["razorpay_order_id"],
                    "razorpay_payment_id": data["razorpay_payment_id"],
                    "razorpay_signature": data["razorpay_signature"],
                }
            )

            with transaction.atomic():
                payment = Payment.objects.get(
                    razorpay_order_id=data["razorpay_order_id"]
                )

                if payment.status == "success":
                    return Response(
                        {"message": "Payment already processed"},
                        status=status.HTTP_200_OK,
                    )

                payment.razorpay_payment_id = data["razorpay_payment_id"]
                payment.status = "success"
                payment.save()

                new_xp = XPService.add_xp(
                    user=request.user,
                    amount=payment.xp_amount,
                    source=XPService.SOURCE_PURCHASE,
                )

            return Response(
                {"status": "success", "new_xp": new_xp}, status=status.HTTP_200_OK
            )

        except razorpay.errors.SignatureVerificationError:
            return Response(
                {"error": "Invalid Signature - Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Payment.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
