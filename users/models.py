from django.contrib.auth.models import AbstractUser
from django.db import models

from django_jalali.db import models as jmodels


class User(AbstractUser):
    """مدل کاربر برای مدیریت اعضای صندوق"""
    is_admin = models.BooleanField(default=False)
    join_date = jmodels.jDateTimeField(auto_now_add=True)  # ذخیره بر اساس تایم تهران

    # def join_date_jalali(self):
    #     """تبدیل تاریخ عضویت به شمسی"""
    #     return jdatetime.datetime.fromgregorian(datetime=localtime(self.join_date))

    def __str__(self):
        return self.username
