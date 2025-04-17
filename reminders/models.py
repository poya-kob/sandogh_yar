from django.db import models
from django.core.mail import send_mail

from django_jalali.db import models as jmodels
from loans.models import LoanRequest, InstallmentPayment
from users.models import User


class Reminder(models.Model):
    """مدل مربوط به یادآوری پرداخت اقساط و حق عضویت"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_type = models.CharField(
        max_length=20,
        choices=[("loan", "قسط وام"), ("membership", "حق عضویت")],
    )
    due_date = jmodels.jDateField()  # تاریخ سررسید پرداخت
    sent = models.BooleanField(default=False)  # آیا یادآوری ارسال شده؟

    def send_email_reminder(self):
        """ارسال ایمیل یادآوری"""
        subject = "یادآوری پرداخت"
        message = f"""
        کاربر عزیز {self.user.get_full_name()}،
        لطفاً پرداخت {self.get_reminder_type_display()} خود را تا تاریخ {self.due_date} انجام دهید.
        """
        send_mail(subject, message, "noreply@sandoghyar.com", [self.user.email])
        self.sent = True
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.get_reminder_type_display()} ({self.due_date})"
