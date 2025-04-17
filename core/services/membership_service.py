from payments.models import MembershipFee
import jdatetime


def create_new_membership_fee(amount, start_date):
    # بستن مبلغ قبلی
    previous_fee = MembershipFee.objects.filter(end_date__isnull=True).first()
    if previous_fee:
        previous_fee.end_date = start_date - jdatetime.timedelta(days=1)
        previous_fee.save()

    # ساخت مبلغ جدید
    return MembershipFee.objects.create(amount=amount, start_date=start_date)


def create_new_fee():
    # todo: set end_date of last fee
    pass


def get_current_fee(date):
    pass
