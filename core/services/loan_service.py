from django.db import transaction
from django.db.models import F

from loans.models import LoanRequest, InstallmentPayment


def payed_loan_process(instance: LoanRequest):
    with transaction.atomic():
        instance.calculate_installment()
        instance.remaining = instance.amount
        instance.save()
        instance.create_installment_schedule()

        fund = instance.fund
        fund.total_fund = F('total_fund') - instance.amount
        fund.save(update_fields=['total_fund'])


def installment_process(instance: InstallmentPayment):
    with transaction.atomic():
        installment = instance.installment
        loan = installment.loan
        fund = loan.fund

        installment.is_payed = True
        installment.save(update_fields=['is_payed'])

        fund.total_fund = F('total_fund') + instance.amount
        fund.save(update_fields=['total_fund'])

        loan.remaining = F('remaining') - instance.amount
        loan.save(update_fields=['remaining'])
