from django.contrib.auth.models import AbstractUser
from django.db import models

from django_jalali.db import models as jmodels


class User(AbstractUser):
    """مدل کاربر برای مدیریت اعضای صندوق"""
    is_admin = models.BooleanField(default=False)
    join_date = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# todo:users must have profile to save balance and pic and ...
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile', null=True, blank=True)
    next_payment_date = jmodels.jDateField()


class BalanceSheet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    total_paid = models.PositiveIntegerField(default=0)  # کل پرداخت‌ها
    total_due = models.PositiveIntegerField(default=0)  # کل بدهی ( وام + حق عضویت)
