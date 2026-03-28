from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import BackInStockNotification, OutOfStockReservation

def get_stock_status(product, item_type):
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
    if not user.is_authenticated:
        return False

    try:
        if item_type == 'cloth':
            return BackInStockNotification.objects.filter(
                user=user,
                cloth=product,
                is_active=True
            ).exists()
        else:
            return BackInStockNotification.objects.filter(
                user=user,
                toy=product,
                is_active=True
            ).exists()
    except:
        return False

def has_reservation(user, product, item_type):
    if not user.is_authenticated:
        return False

    try:
        if item_type == 'cloth':
            return OutOfStockReservation.objects.filter(
                user=user,
                cloth=product,
                status__in=['pending', 'notified']
            ).exists()
        else:
            return OutOfStockReservation.objects.filter(
                user=user,
                toy=product,
                status__in=['pending', 'notified']
            ).exists()
    except:
        return False

def clean_expired_reservations():
    cutoff_date = timezone.now() - timedelta(days=30)
    return OutOfStockReservation.objects.filter(
        created_at__lt=cutoff_date,
        status='pending'
    ).update(status='cancelled')

def notify_back_in_stock(product, item_type):
    from django.core.mail import send_mail
    from django.conf import settings

    if item_type == 'cloth':
        notifications = BackInStockNotification.objects.filter(
            cloth=product,
            is_active=True
        )
    else:
        notifications = BackInStockNotification.objects.filter(
            toy=product,
            is_active=True
        )

    for notif in notifications:
        try:
            subject = f"✓ {product.name} is Back in Stock!"

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [notif.user.email],
                fail_silently=True
            )

            notif.is_active = False
            notif.save()

        except Exception as e:
            print(f"Error sending back-in-stock notification: {e}")

def notify_reservation_ready(reservation):
    from django.core.mail import send_mail
    from django.conf import settings

    try:
        product = reservation.get_product()

        subject = f"Reserved: {product.name} is Ready to Purchase!"

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
    if item_type == 'cloth':
        return OutOfStockReservation.objects.filter(
            cloth=product,
            status__in=['pending', 'notified']
        ).count()
    else:
        return OutOfStockReservation.objects.filter(
            toy=product,
            status__in=['pending', 'notified']
        ).count()
