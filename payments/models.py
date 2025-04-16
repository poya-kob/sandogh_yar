from django.db import models

from django_jalali.db import models as jmodels
from users.models import User


class MembershipFee(models.Model):
    """مدل مربوط به حق عضویت ماهانه که توسط ادمین تعیین می‌شود"""
    amount = models.PositiveIntegerField()  # مبلغ حق عضویت
    start_date = jmodels.jDateField()  # تاریخ شروع این مبلغ
    end_date = jmodels.jDateField(null=True, blank=True)  # تاریخ پایان (در صورت تغییر مبلغ)

    def __str__(self):
        return f"{self.amount} تومان از {self.start_date}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
        # todo: set end_date on last obj = current object start_date


class Payment(models.Model):
    """مدل مربوط به پرداخت‌های کاربران"""
    STATUS_CHOICES = (
        ('PR', 'درانتظار بررسی'),
        ('R', 'تایید نشده'),
        ('A', 'تایید شده'),
        ('U', 'پرداخت نشده'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # مبلغ پرداختی
    payment_date = jmodels.jDateTimeField(auto_now_add=True)  # تاریخ پرداخت
    receipt_image = models.ImageField(upload_to="receipts/", null=True, blank=True)  # تصویر فیش پرداختی
    payment_status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='U')  # وضعیت پرداخت

    def __str__(self):
        return f"{self.user.username} - {self.amount} تومان ({self.payment_date})"


class BalanceSheet(models.Model):
    """مدل ترازنامه برای ثبت وضعیت مالی صندوق"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_paid = models.PositiveIntegerField(default=0)  # کل مبلغ پرداخت ‌شده
    remaining_balance = models.PositiveIntegerField(default=0)  # موجودی باقی‌مانده یا بدهی

    def __str__(self):
        return f"{self.user.username} - موجودی: {self.remaining_balance} تومان"
