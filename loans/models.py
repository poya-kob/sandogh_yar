from django.db import models

from django_jalali.db import models as jmodels
from users.models import User


class LoanRequest(models.Model):
    """مدل مربوط به درخواست وام توسط کاربران"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # مبلغ وام
    request_date = jmodels.jDateTimeField(auto_now_add=True)  # تاریخ درخواست
    is_approved = models.BooleanField(default=False)  # وضعیت تأیید ادمین
    approval_date = jmodels.jDateTimeField(null=True, blank=True)  # تاریخ تأیید وام
    repayment_months = models.PositiveIntegerField(default=20)  # تعداد ماه‌های بازپرداخت (ثابت: 20 ماه)
    monthly_installment = models.PositiveIntegerField(null=True, blank=True)  # مبلغ هر قسط

    def calculate_installment(self):
        """محاسبه مبلغ هر قسط (تقسیم مبلغ وام بر 20 ماه)"""
        self.monthly_installment = self.amount // 20

    def save(self, *args, **kwargs):
        self.calculate_installment()
        super().save(*args, **kwargs)


class LoanPayment(models.Model):
    """مدل مربوط به پرداخت اقساط وام"""
    loan = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # مبلغ پرداخت‌شده
    payment_date = jmodels.jDateTimeField(auto_now_add=True)  # تاریخ پرداخت
    receipt_image = models.ImageField(upload_to="loan_receipts/", null=True, blank=True)  # تصویر فیش پرداختی
    is_approved = models.BooleanField(default=False)  # تأیید پرداخت توسط ادمین

    # def payment_date_jalali(self):
    #     return jdatetime.datetime.fromgregorian(datetime=localtime(self.payment_date)).strftime("%Y/%m/%d - %H:%M")

    def __str__(self):
        return f"{self.loan.user.username} - قسط {self.amount} تومان ({self.payment_date})"
