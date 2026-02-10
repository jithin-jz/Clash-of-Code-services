"""
Certificate Generator Service
Generates professional certificates with QR codes for verification.
"""
import io
import uuid
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.core.files.base import ContentFile
from django.conf import settings
from .models import UserCertificate, UserProgress


class CertificateGenerator:
    """Generate professional certificates for users who complete 49 challenges"""
    
    # Certificate dimensions
    WIDTH = 1920
    HEIGHT = 1080
    
    # Colors (matching the design)
    COLOR_BACKGROUND = '#FFFEF9'  # Cream/Off-white
    COLOR_BORDER_GOLD = '#8B6F47'  # Brown/Gold
    COLOR_TEXT_BLACK = '#000000'  # Black
    COLOR_TEXT_GRAY = '#666666'  # Gray
    
    def __init__(self):
        self.width = self.WIDTH
        self.height = self.HEIGHT
    
    def generate_certificate(self, user):
        """
        Generate certificate for a user who has completed 49+ challenges.
        Returns UserCertificate instance with generated image.
        """
        # Check if certificate already exists
        try:
            certificate = UserCertificate.objects.get(user=user)
            return certificate
        except UserCertificate.DoesNotExist:
            pass
        
        # Count completed challenges
        completed_count = UserProgress.objects.filter(
            user=user,
            status=UserProgress.Status.COMPLETED
        ).count()
        
        if completed_count < 49:
            raise ValueError(f"User has only completed {completed_count} challenges. Need 49 to generate certificate.")
        
        # Create certificate record
        certificate = UserCertificate.objects.create(
            user=user,
            completion_count=completed_count
        )
        
        # Generate certificate image
        img = self._create_certificate_image(user, certificate)
        
        # Save image to model
        img_io = io.BytesIO()
        img.save(img_io, format='PNG', quality=95)
        img_io.seek(0)
        
        filename = f'certificate_{user.username}_{certificate.certificate_id}.png'
        certificate.certificate_image.save(filename, ContentFile(img_io.read()), save=True)
        
        return certificate
    
    def _create_certificate_image(self, user, certificate):
        """Create the actual certificate image with all design elements"""
        # Create base image
        img = Image.new('RGB', (self.width, self.height), self.COLOR_BACKGROUND)
        draw = ImageDraw.Draw(img)
        
        # Draw double-line gold border
        self._draw_borders(draw)
        
        # Add text content
        self._add_text_content(draw, user)
        
        # Add QR code
        self._add_qr_code(img, certificate.verification_url)
        
        # Add signature lines
        self._add_signatures(draw)
        
        return img
    
    def _draw_borders(self, draw):
        """Draw decorative double-line border"""
        padding_outer = 40
        padding_inner = 55
        
        # Outer border
        draw.rectangle(
            [padding_outer, padding_outer, self.width - padding_outer, self.height - padding_outer],
            outline=self.COLOR_BORDER_GOLD,
            width=8
        )
        
        # Inner border
        draw.rectangle(
            [padding_inner, padding_inner, self.width - padding_inner, self.height - padding_inner],
            outline=self.COLOR_BORDER_GOLD,
            width=3
        )
    
    def _add_text_content(self, draw, user):
        """Add all text content to certificate"""
        center_x = self.width // 2
        
        # Title: "CERTIFICATE OF COMPLETION"
        title_font = self._get_font(size=100, bold=True)
        title_text = "CERTIFICATE OF COMPLETION"
        self._draw_centered_text(draw, title_text, center_x, 180, title_font, self.COLOR_TEXT_BLACK)
        
        # "This certifies that"
        subtitle_font = self._get_font(size=45)
        self._draw_centered_text(draw, "This certifies that", center_x, 300, subtitle_font, self.COLOR_TEXT_GRAY)
        
        # User's name (large, decorative)
        name_font = self._get_font(size=120, bold=True)
        user_name = user.username.upper()
        self._draw_centered_text(draw, user_name, center_x, 420, name_font, self.COLOR_BORDER_GOLD)
        
        # "Has successfully completed the"
        self._draw_centered_text(draw, "Has successfully completed the", center_x, 560, subtitle_font, self.COLOR_TEXT_GRAY)
        
        # "PYTHON MASTERY COURSE"
        course_font = self._get_font(size=90, bold=True)
        self._draw_centered_text(draw, "PYTHON MASTERY COURSE", center_x, 660, course_font, self.COLOR_TEXT_BLACK)
        
        # Date
        from datetime import datetime
        date_text = datetime.now().strftime("%B %d, %Y")
        date_font = self._get_font(size=40)
        self._draw_centered_text(draw, date_text, center_x, 780, date_font, self.COLOR_TEXT_GRAY)
    
    def _add_signatures(self, draw):
        """Add signature sections"""
        # Left signature - Jithin (CEO & Founder)
        left_x = 350
        y_pos = 900
        
        sig_font = self._get_font(size=50, italic=True)
        label_font = self._get_font(size=28)
        
        # Jithin signature
        draw.text((left_x, y_pos), "Jithin", font=sig_font, fill=self.COLOR_TEXT_BLACK, anchor="mm")
        draw.line([(left_x - 150, y_pos + 50), (left_x + 150, y_pos + 50)], fill=self.COLOR_TEXT_BLACK, width=2)
        draw.text((left_x, y_pos + 80), "CEO & Founder", font=label_font, fill=self.COLOR_TEXT_GRAY, anchor="mm")
        
        # Right signature - Code of Clans
        right_x = self.width - 350
        draw.text((right_x, y_pos), "Code of Clans", font=sig_font, fill=self.COLOR_TEXT_BLACK, anchor="mm")
        draw.line([(right_x - 150, y_pos + 50), (right_x + 150, y_pos + 50)], fill=self.COLOR_TEXT_BLACK, width=2)
        draw.text((right_x, y_pos + 80), "Platform", font=label_font, fill=self.COLOR_TEXT_GRAY, anchor="mm")
    
    def _add_qr_code(self, img, verification_url):
        """Generate and add QR code to certificate"""
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((200, 200))
        
        # Add white background for QR code
        qr_background = Image.new('RGB', (220, 220), 'white')
        qr_background.paste(qr_img, (10, 10))
        
        # Paste QR code at bottom center
        qr_x = (self.width - 220) // 2
        qr_y = self.height - 280
        img.paste(qr_background, (qr_x, qr_y))
    
    def _get_font(self, size=40, bold=False, italic=False):
        """Get font with fallback to default"""
        try:
            # Try to use system fonts
            if bold and italic:
                return ImageFont.truetype("arialbi.ttf", size)
            elif bold:
                return ImageFont.truetype("arialbd.ttf", size)
            elif italic:
                return ImageFont.truetype("ariali.ttf", size)
            else:
                return ImageFont.truetype("arial.ttf", size)
        except:
            # Fallback to default font
            return ImageFont.load_default()
    
    def _draw_centered_text(self, draw, text, x, y, font, color):
        """Draw text centered at given position"""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = x - (text_width // 2)
        draw.text((text_x, y), text, font=font, fill=color)
    
    @staticmethod
    def is_eligible(user):
        """Check if user is eligible for a certificate"""
        completed_count = UserProgress.objects.filter(
            user=user,
            status=UserProgress.Status.COMPLETED
        ).count()
        return completed_count >= 49
