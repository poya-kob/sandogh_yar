from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LoanRequest, InstallmentPayment, InstallmentSchedule

from reminders.tasks.loan_reminders import notify_loan_deposit, notify_loan_status, notify_new_request_to_admin, \
    notify_installment_status


@receiver(post_save, sender=LoanRequest)
def schedule_admin_notification(sender, instance, created, **kwargs):
    # سیگنال راه اندازی فرایند اقدامات ادمین بر روی درخواست وام
    if created:
        # درخواست وام جدید به ادمین اطلاع داده میشود
        notify_new_request_to_admin.delay(instance)

    dirty_fields: dict = instance.get_dirty_fields()
    if 'request_status' in dirty_fields:
        # اعلامیه تغییر وضعیت درخواست وام به کاربر
        notify_loan_status.delay(instance)
    if 'is_payed' in dirty_fields:
        # اعلامیه واریز وام به حساب کاربر
        notify_loan_deposit.delay(instance)


@receiver(post_save, sender=InstallmentPayment)
def handle_installment_payment_update(sender, instance, created, **kwargs):
    dirty_fields: dict = instance.get_dirty_fields()
    if 'installment_status' in dirty_fields:
        notify_installment_status.delay(instance)


@receiver(post_save, sender=InstallmentSchedule)
def schedule_reminder_on_installment_create(sender, instance, created, **kwargs):
    if created:
        # تسک رو اجرا کن، مثلاً یک هفته قبل از موعد
        instance.schedule_reminder()
