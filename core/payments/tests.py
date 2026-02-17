from unittest.mock import patch
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Payment


class VerifyPaymentSecurityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="buyer", password="password")
        self.other_user = User.objects.create_user(username="other", password="password")
        self.url = reverse("verify-payment")

    @patch("payments.views.client.utility.verify_payment_signature")
    @patch("payments.views.XPService.add_xp")
    def test_rejects_verification_for_other_users_order(self, mock_add_xp, mock_verify_signature):
        payment = Payment.objects.create(
            user=self.other_user,
            razorpay_order_id="order_test_1",
            amount=99,
            xp_amount=100,
            status="pending",
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url,
            {
                "razorpay_order_id": payment.razorpay_order_id,
                "razorpay_payment_id": "pay_test_1",
                "razorpay_signature": "sig_test_1",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        payment.refresh_from_db()
        self.assertEqual(payment.status, "pending")
        mock_add_xp.assert_not_called()

    @patch("payments.views.client.utility.verify_payment_signature")
    @patch("payments.views.XPService.add_xp", return_value=200)
    def test_idempotent_success_does_not_recredit_xp(self, mock_add_xp, mock_verify_signature):
        payment = Payment.objects.create(
            user=self.user,
            razorpay_order_id="order_test_2",
            amount=99,
            xp_amount=100,
            status="pending",
        )
        self.client.force_authenticate(user=self.user)

        payload = {
            "razorpay_order_id": payment.razorpay_order_id,
            "razorpay_payment_id": "pay_test_2",
            "razorpay_signature": "sig_test_2",
        }
        first = self.client.post(self.url, payload, format="json")
        second = self.client.post(self.url, payload, format="json")

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(mock_add_xp.call_count, 1)
