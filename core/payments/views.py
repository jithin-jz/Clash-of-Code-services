import razorpay
from django.conf import settings
from django.db import transaction
from rest_framework import views, status, permissions
from rest_framework.response import Response

from .models import Payment
from .serializers import CreateOrderSerializer, VerifyPaymentSerializer
from xpoint.services import XPService  # Centralized XP handling service


# -------------------------------------------------------------------
# Razorpay Client Initialization
# -------------------------------------------------------------------
# Uses credentials from Django settings to authenticate API requests
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


# -------------------------------------------------------------------
# Create Order View
# -------------------------------------------------------------------
class CreateOrderView(views.APIView):
    """
    Creates a Razorpay order for purchasing XP.

    Flow:
    - Validate requested amount
    - Create Razorpay order (amount in paise)
    - Map amount to XP package
    - Store pending Payment record
    - Return order details to frontend
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)

        if serializer.is_valid():
            amount_inr = serializer.validated_data['amount']

            # Razorpay expects amount in paise
            data = {
                "amount": amount_inr * 100,
                "currency": "INR",
                "notes": {
                    "user_id": request.user.id
                }
            }

            try:
                # Create Razorpay order
                order = client.order.create(data=data)

                # XP packages mapped to price
                XP_PACKAGES_MAP = {
                    99: 100,
                    249: 250,
                    499: 500,
                    999: 1000,
                }

                # Validate requested package
                if amount_inr not in XP_PACKAGES_MAP:
                    return Response(
                        {'error': 'Invalid package amount'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                xp_to_credit = XP_PACKAGES_MAP[amount_inr]

                # Persist pending payment record
                Payment.objects.create(
                    user=request.user,
                    razorpay_order_id=order['id'],
                    amount=amount_inr,
                    xp_amount=xp_to_credit,
                    status='pending'
                )

                # Return order info to frontend
                return Response(
                    {
                        'order_id': order['id'],
                        'amount': data['amount'],
                        'key': settings.RAZORPAY_KEY_ID,
                        'xp_amount': xp_to_credit,
                    },
                    status=status.HTTP_201_CREATED
                )

            except Exception as e:
                # Any Razorpay or unexpected failure
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Serializer validation failed
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------
# Verify Payment View
# -------------------------------------------------------------------
class VerifyPaymentView(views.APIView):
    """
    Verifies Razorpay payment and credits XP.

    Flow:
    - Validate signature from Razorpay
    - Ensure payment is not already processed
    - Mark payment as successful
    - Credit XP using XPService
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VerifyPaymentSerializer

    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            try:
                # Verify Razorpay signature
                client.utility.verify_payment_signature({
                    'razorpay_order_id': data['razorpay_order_id'],
                    'razorpay_payment_id': data['razorpay_payment_id'],
                    'razorpay_signature': data['razorpay_signature'],
                })

                # Atomic block to avoid double-crediting XP
                with transaction.atomic():
                    payment = Payment.objects.get(
                        razorpay_order_id=data['razorpay_order_id']
                    )

                    # Idempotency check
                    if payment.status == 'success':
                        return Response(
                            {'message': 'Payment already processed'},
                            status=status.HTTP_200_OK
                        )

                    # Mark payment as successful
                    payment.razorpay_payment_id = data['razorpay_payment_id']
                    payment.status = 'success'
                    payment.save()

                    # Credit XP through centralized service
                    new_xp = XPService.add_xp(
                        user=request.user,
                        amount=payment.xp_amount,
                        source=XPService.SOURCE_PURCHASE
                    )

                return Response(
                    {'status': 'success', 'new_xp': new_xp},
                    status=status.HTTP_200_OK
                )

            except razorpay.errors.SignatureVerificationError:
                return Response(
                    {'error': 'Invalid Signature'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            except Payment.DoesNotExist:
                return Response(
                    {'error': 'Order not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Serializer validation failed
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
