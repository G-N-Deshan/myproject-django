"""
Utils for Stock Indicator System
Handles stock status, notifications, and reservations
"""

from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import BackInStockNotification, OutOfStockReservation


def get_stock_status(product, item_type):
    """
    Get stock status badge and message for a product.
    
    Returns:
        dict: {
            'badge_class': 'in-stock|low-stock|out-of-stock',
            'badge_text': 'In Stock' or 'Only 3 left!' or 'Out of Stock',
            'is_in_stock': bool,
            'is_low_stock': bool,
            'stock_level': int
        }
    """
    stock = getattr(product, 'stock_quantity', 100)
    
    if stock <= 0:
        return {
            'badge_class': 'out-of-stock',
            'badge_text': 'Out of Stock',
            'is_in_stock': False,
            'is_low_stock': False,
            'stock_level': 0
        }
    elif stock <= 5:
        return {
            'badge_class': 'low-stock',
            'badge_text': f'Only {stock} left!',
            'is_in_stock': True,
            'is_low_stock': True,
            'stock_level': stock
        }
    else:
        return {
            'badge_class': 'in-stock',
            'badge_text': 'In Stock',
            'is_in_stock': True,
            'is_low_stock': False,
            'stock_level': stock
        }


def has_back_in_stock_alert(user, product, item_type):
    """Check if user has an active back-in-stock notification"""
    if not user.is_authenticated:
        return False
    
    try:
        if item_type == 'cloth':
            return BackInStockNotification.objects.filter(
                user=user, 
                cloth=product, 
                is_active=True
            ).exists()
        else:  # toy
            return BackInStockNotification.objects.filter(
                user=user, 
                toy=product, 
                is_active=True
            ).exists()
    except:
        return False


def has_reservation(user, product, item_type):
    """Check if user has a pending/notified reservation"""
    if not user.is_authenticated:
        return False
    
    try:
        if item_type == 'cloth':
            return OutOfStockReservation.objects.filter(
                user=user,
                cloth=product,
                status__in=['pending', 'notified']
            ).exists()
        else:  # toy
            return OutOfStockReservation.objects.filter(
                user=user,
                toy=product,
                status__in=['pending', 'notified']
            ).exists()
    except:
        return False


def clean_expired_reservations():
    """Remove expired reservations (older than 30 days without action)"""
    cutoff_date = timezone.now() - timedelta(days=30)
    return OutOfStockReservation.objects.filter(
        created_at__lt=cutoff_date,
        status='pending'
    ).update(status='cancelled')


def notify_back_in_stock(product, item_type):
    """
    Send notifications to all users who requested back-in-stock alerts.
    Called when product stock > 0 and was previously out of stock.
    """
    from django.core.mail import send_mail
    from django.conf import settings
    
    if item_type == 'cloth':
        notifications = BackInStockNotification.objects.filter(
            cloth=product,
            is_active=True
        )
    else:  # toy
        notifications = BackInStockNotification.objects.filter(
            toy=product,
            is_active=True
        )
    
    for notif in notifications:
        try:
            # Send email
            subject = f"✓ {product.name} is Back in Stock!"
            message = f"""
            Hi {notif.user.first_name or notif.user.username},

            Great news! {product.name} is now back in stock and available for purchase.

            View Product: {settings.SITE_URL}/product/{item_type}/{product.id}/

            Limited stock available - don't wait!

            Best regards,
            KidZone Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [notif.user.email],
                fail_silently=True
            )
            
            # Mark notification as sent
            notif.is_active = False
            notif.save()
            
        except Exception as e:
            # Log error but continue with other notifications
            print(f"Error sending back-in-stock notification: {e}")


def notify_reservation_ready(reservation):
    """
    Send notification to user that their reserved item is ready for purchase.
    Called when product comes back in stock or quantity becomes available.
    """
    from django.core.mail import send_mail
    from django.conf import settings
    
    try:
        product = reservation.get_product()
        
        subject = f"Reserved: {product.name} is Ready to Purchase!"
        message = f"""
        Hi {reservation.user.first_name or reservation.user.username},

        Your reserved item is now back in stock!

        Product: {product.name}
        Quantity: {reservation.quantity}
        Size: {reservation.size or 'N/A'}
        Color: {reservation.color or 'N/A'}

        This reservation will expire in 7 days if not purchased.

        Get it now: {settings.SITE_URL}/product/{'toy' if hasattr(product, 'age_range') else 'cloth'}/{product.id}/

        Best regards,
        KidZone Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [reservation.email],
            fail_silently=True
        )
        
        reservation.mark_as_notified()
        
    except Exception as e:
        print(f"Error sending reservation notification: {e}")


def get_reservation_count(product, item_type):
    """Get number of pending reservations for a product"""
    if item_type == 'cloth':
        return OutOfStockReservation.objects.filter(
            cloth=product,
            status__in=['pending', 'notified']
        ).count()
    else:  # toy
        return OutOfStockReservation.objects.filter(
            toy=product,
            status__in=['pending', 'notified']
        ).count()
