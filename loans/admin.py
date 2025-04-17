import django_jalali.admin as jadmin
from django.contrib import admin
from .models import LoanRequest, InstallmentPayment


@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user", "amount", "request_date", "is_approved", "approval_date", "monthly_installment")
    list_filter = ("is_approved", "request_date")


@admin.register(InstallmentPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ("loan", "amount", "payment_date", "is_approved")
    list_filter = ("is_approved", "payment_date")
