from django.core.exceptions import ValidationError
from django.db import models
from django_jalali.db import models as jmodels
from users.models import User
from django.utils.crypto import get_random_string

from utils.bank_info_validations import is_valid_card_number


class Fund(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='fund_logos/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_funds')
    admins = models.ManyToManyField(User, related_name='admin_funds', blank=True, null=True)
    join_code = models.CharField(max_length=8, unique=True, default=get_random_string)
    foundation_year = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    total_fund = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.join_code})"


class FundBankInfo(models.Model):
    fund = models.ForeignKey("Fund", on_delete=models.CASCADE, related_name="bank_info")
    bank_name = models.CharField(max_length=100)  # todo: set bank name automatically
    account_number = models.CharField(max_length=30, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    iban = models.CharField("شماره شبا", max_length=26, null=True, blank=True)
    payment_identifier = models.CharField("شناسه پرداخت", max_length=50, blank=True, null=True, )
    is_active = models.BooleanField(default=True)

    def clean(self):
        # todo: اعتبار سنجی برای همه
        # اعتبارسنجی شماره کارت (مثلاً با الگوریتم لوه یا regex)
        if self.card_number and not is_valid_card_number(self.card_number):
            raise ValidationError("شماره کارت معتبر نیست.")

        # اعتبارسنجی شماره شبا
        if self.iban and not self.iban.startswith("IR"):
            raise ValidationError("شماره شبا باید با IR شروع شود.")

    def __str__(self):
        return f"{self.bank_name} - {self.iban}"
