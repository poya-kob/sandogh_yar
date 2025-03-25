import jdatetime
from django.utils.timezone import localtime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """مدل کاربر برای مدیریت اعضای صندوق"""
    is_admin = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)  # ذخیره بر اساس تایم تهران

    def join_date_jalali(self):
        """تبدیل تاریخ عضویت به شمسی"""
        return jdatetime.datetime.fromgregorian(datetime=localtime(self.join_date))

    def __str__(self):
        return self.username
