from celery import shared_task
from core.services.loan_service import installment_process, payed_loan_process
from loans.models import InstallmentSchedule
from reminders.notifications import send_reminder


@shared_task
def notify_loan_deposit():
    # todo: اعلامیه واریز وام به کاربر
    pass


@shared_task
def notify_installment_status(instance):
    # todo: اعلامیه تغییر وضعیت فیش واریزی وام به کاربر
    if instance.installment_status == 'A':
        installment_process(instance)


@shared_task
def notify_loan_status(instance):
    # todo: اعلامیه تغییر وضعیت درخواست وام به کاربر
    if instance.request_status == 'A' and instance.is_payed:
        payed_loan_process(instance)


@shared_task
def notify_new_request_to_admin():
    # todo: اعلامیه ثبت درخواست وام جدید به ادمین
    pass


@shared_task
def schedule_installment_reminder(installment_id):
    try:
        installment = InstallmentSchedule.objects.get(id=installment_id)
        user = installment.loan.user
        due_date = installment.due_date
        amount = installment.amount

        message = f"یادآوری: قسط {amount} تومان شما در تاریخ {due_date} سررسید می‌شود."
        send_reminder(user, message)

    except InstallmentSchedule.DoesNotExist:
        # یا لاگ بزن یا بی‌خیال شو
        pass
