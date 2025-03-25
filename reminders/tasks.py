from celery import shared_task
from django.utils.timezone import localtime
from .models import UserSubscription


@shared_task
def send_payment_reminders():
    today = localtime().date()
    users = UserSubscription.objects.filter(next_payment_due=today)

    for user in users:
        # ارسال پیامک یا ایمیل (اینجا باید پیاده‌سازی بشه)
        print(f"Reminder sent to {user.user.phone_number}")
