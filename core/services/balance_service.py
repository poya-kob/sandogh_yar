from payments.models import Payment
from payments.models import MembershipFee
from users.models import BalanceSheet
from django.db.models import Sum
import jdatetime


def calculate_total_membership_fee():
    today = jdatetime.date.today()
    total = 0
    for fee in MembershipFee.objects.all():
        if fee.start_date <= today and (not fee.end_date or fee.end_date >= fee.start_date):
            total += fee.amount
    return total


def update_user_balance(user):
    total_paid = Payment.objects.filter(user=user, payment_status='A').aggregate(Sum('amount'))['amount__sum'] or 0
    total_fee = calculate_total_membership_fee()
    BalanceSheet.objects.update_or_create(user=user, defaults={
        'total_paid': total_paid,
        'remaining_balance': total_paid - total_fee
    })


def calculate_fund_balance():
    # todo: حساب کردن کل موجودی صندوق
    pass
