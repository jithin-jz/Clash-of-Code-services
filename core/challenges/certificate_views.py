"""
Certificate API ViewSet
"""
from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

from .models import UserCertificate
from .serializers import UserCertificateSerializer
from .certificate_generator import CertificateGenerator


class CertificateViewSet(viewsets.ViewSet):
    """API endpoints for certificate generation and verification"""
    
    permission_classes = [IsAuthenticated]
    
    @decorators.action(detail=False, methods=['get'])
    def my_certificate(self, request):
        """
        Get or generate certificate for the authenticated user.
        GET /api/certificates/my_certificate/
        """
        user = request.user
        generator = CertificateGenerator()
        
        # Check if user is eligible
        if not generator.is_eligible(user):
            return Response(
                {"error": "You need to complete 53 challenges to earn a certificate."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Try to get existing certificate
            certificate = UserCertificate.objects.get(user=user)
        except UserCertificate.DoesNotExist:
            # Generate new certificate
            try:
                certificate = generator.generate_certificate(user)
            except Exception as e:
                logger.error(f"Failed to generate certificate for {user.username}: {e}")
                return Response(
                    {"error": "Failed to generate certificate. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        serializer = UserCertificateSerializer(certificate, context={'request': request})
        return Response(serializer.data)
    
    @decorators.action(detail=False, methods=['get'], url_path='verify/(?P<certificate_id>[^/.]+)', permission_classes=[AllowAny])
    def verify(self, request, certificate_id=None):
        """
        Verify a certificate by its ID.
        GET /api/certificates/verify/<certificate_id>/
        Public endpoint - no authentication required.
        """
        try:
            certificate = get_object_or_404(UserCertificate, certificate_id=certificate_id)
            serializer = UserCertificateSerializer(certificate, context={'request': request})
            return Response({
                "valid": certificate.is_valid,
                "certificate": serializer.data
            })
        except Exception as e:
            logger.error(f"Certificate verification error: {e}")
            return Response(
                {"valid": False, "error": "Certificate not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @decorators.action(detail=False, methods=['get'])
    def download(self, request):
        """
        Download certificate image.
        GET /api/certificates/download/
        """
        user = request.user
        
        try:
            certificate = UserCertificate.objects.get(user=user)
            
            if not certificate.certificate_image:
                return Response(
                    {"error": "Certificate image not generated yet"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Return image file
            response = HttpResponse(certificate.certificate_image.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="certificate_{user.username}.png"'
            return response
            
        except UserCertificate.DoesNotExist:
            return Response(
                {"error": "No certificate found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @decorators.action(detail=False, methods=['get'])
    def check_eligibility(self, request):
        """
        Check if user is eligible for certificate.
        GET /api/certificates/check_eligibility/
        """
        user = request.user
        generator = CertificateGenerator()
        
        from .models import UserProgress
        completed_count = UserProgress.objects.filter(
            user=user,
            status=UserProgress.Status.COMPLETED
        ).count()
        
        return Response({
            "eligible": generator.is_eligible(user),
            "completed_challenges": completed_count,
            "required_challenges": 53,
            "has_certificate": UserCertificate.objects.filter(user=user).exists()
        })
