from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VitalsMonitor:
    @staticmethod
    def check_thresholds(vital_type: str, value: float) -> tuple[bool, str]:
        """
        Check if a vital sign is within normal range.
        Returns (is_alert, message)
        """
        thresholds = settings.VITAL_SIGNS_SETTINGS.get(vital_type.upper())
        if not thresholds:
            return False, ""
            
        min_threshold = thresholds['MIN_THRESHOLD']
        max_threshold = thresholds['MAX_THRESHOLD']
        
        if value < min_threshold:
            return True, f"{vital_type} is below normal range: {value} (Min: {min_threshold})"
        elif value > max_threshold:
            return True, f"{vital_type} is above normal range: {value} (Max: {max_threshold})"
        
        return False, ""

    @staticmethod
    def send_alert(message: str, vital_type: str, value: float) -> bool:
        """
        Send email alert with cooldown period to prevent alert fatigue.
        Returns True if alert was sent.
        """
        cache_key = f"alert_{vital_type.lower()}_{value:.1f}"
        
        # Check if we've recently sent an alert for this condition
        if cache.get(cache_key):
            return False
            
        try:
            subject = f"ALERT: Abnormal {vital_type} Reading"
            email_body = (
                f"Warning: {message}\n"
                f"Timestamp: {datetime.now()}\n"
                f"Please check the patient immediately."
            )
            
            send_mail(
                subject=subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=settings.EMAIL_ALERT_SETTINGS['ALERT_EMAILS'],
                fail_silently=False,
            )
            
            # Set cache to prevent repeated alerts
            cache.set(
                cache_key, 
                True, 
                settings.EMAIL_ALERT_SETTINGS['ALERT_COOLDOWN']
            )
            
            logger.info(f"Alert sent: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send alert email: {str(e)}")
            return False