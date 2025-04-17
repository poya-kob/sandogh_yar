from django.db import models
from datetime import timedelta
from django_jalali.db import models as jmodels
from persiantools.jdatetime import JalaliDate
from users.models import User
from fund.models import Fund, FundBankInfo
from dirtyfields import DirtyFieldsMixin
from utils.jalali_days_in_month import jalali_month_days

from reminders.tasks.loan_reminders import schedule_installment_reminder


class LoanRequest(DirtyFieldsMixin, models.Model):
    STATUS_CHOICES = (
        ('PR', 'درانتظار بررسی'),
        ('R', 'تایید نشده'),
        ('A', 'تایید شده'),
        ('C', 'پرداخت کامل شده'),
    )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # مبلغ وام
    remaining = models.PositiveIntegerField()  # باقیمانده مبلغ وام
    approval_date = jmodels.jDateTimeField(null=True, blank=True)  # تاریخ تایید وام
    repayment_months = models.PositiveIntegerField(default=20)  # تعداد ماه‌های بازپرداخت
    monthly_installment = models.PositiveIntegerField(null=True, blank=True)  # مبلغ هر قسط
    request_date = jmodels.jDateTimeField(auto_now_add=True)  # تاریخ درخواست
    request_status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PR')
    deposit_date_tmp = jmodels.jDateTimeField(null=True, blank=True)  # تاریخ تخمین واریز وام
    is_payed = models.BooleanField(default=False)  # مبلغ وام به حساب کاربر واریز شده
    deposit_date = jmodels.jDateTimeField(null=True, blank=True)  # تاریخ واریز وام

    def calculate_installment(self):
        """
        محاسبه مبلغ هر قسط بر اساس مبلغ وام و تعداد اقساط.
        """
        if self.repayment_months:
            self.monthly_installment = self.amount // self.repayment_months

    def create_installment_schedule(self):
        """
        ایجاد برنامه اقساطی دقیق پس از تایید وام.
        این متد در صورتی اجرا می‌شود که:
          - تاریخ تایید (approval_date) موجود باشد.
          - برنامه اقساطی قبلاً ساخته نشده باشد.

        برای هر قسط، تاریخ سررسید با احتساب ماه شمسی محاسبه می‌شود.
        """
        # اگر تایید نشده یا قبلاً برنامه ساخته شده، ادامه نده
        if not self.approval_date or self.installments.exists():
            return

        # استفاده از تاریخ تایید به عنوان نقطه شروع (بدون بخش زمان)
        start_jdate = JalaliDate(self.approval_date.date())

        for i in range(self.repayment_months):
            # محاسبه سال و ماه برای قسط i‌ام
            new_year = start_jdate.year
            new_month = start_jdate.month + (i + 1)
            while new_month > 12:
                new_month -= 12
                new_year += 1

            # تعیین روز سررسید با توجه به تعداد روزهای ماه جدید
            due_day = min(start_jdate.day, jalali_month_days(new_year, new_month))
            due_jdate = JalaliDate(new_year, new_month, due_day)

            InstallmentSchedule.objects.create(
                loan=self,
                due_date=due_jdate,
                amount=self.monthly_installment
            )

    def __str__(self):
        return f"وام {self.amount} برای {self.user.username}"

    @property
    def paid_installments_count(self):
        return self.installments.filter(is_paid=True).count()

    @property
    def unpaid_installments(self):
        return self.installments.filter(is_paid=False)

    def check_completion(self):
        if self.installments.exists() and not self.installments.filter(is_paid=False).exists():
            self.request_status = 'C'
            self.save(update_fields=['request_status'])


class InstallmentPayment(DirtyFieldsMixin, models.Model):
    """مدل مربوط به پرداخت اقساط وام"""
    STATUS_CHOICES = (
        ('PR', 'درانتظار بررسی'),
        ('R', 'تایید نشده'),
        ('A', 'تایید شده'),
        ('U', 'پرداخت نشده'),
    )
    installment = models.ForeignKey('InstallmentSchedule', on_delete=models.CASCADE)
    bank_info = models.ForeignKey(FundBankInfo, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # مبلغ پرداخت‌شده
    payment_date = jmodels.jDateTimeField(auto_now_add=True)  # تاریخ پرداخت
    receipt_image = models.ImageField(upload_to="loan_receipts/", null=True, blank=True)  # تصویر فیش پرداختی
    installment_status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='U')  # وضعیت پرداخت

    def __str__(self):
        return f"{self.installment.loan.user.username} - قسط {self.amount} تومان ({self.payment_date})"


class InstallmentSchedule(models.Model):
    loan = models.ForeignKey("LoanRequest", on_delete=models.CASCADE, related_name="installments")
    due_date = jmodels.jDateField()
    amount = models.PositiveIntegerField()
    is_payed = models.BooleanField(default=False)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"قسط {self.amount} در {self.due_date}"

    def schedule_reminder(self):
        if not self.due_date:
            return

        notify_date = self.due_date.togregorian().to_datetime() - timedelta(days=7)
        schedule_installment_reminder.apply_async(
            args=[self.id],
            eta=notify_date
        )
