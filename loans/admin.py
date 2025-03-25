from django.contrib import admin
from .models import LoanRequest, LoanPayment


@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user", "amount", "request_date_jalali", "is_approved", "approval_date_jalali", "monthly_installment")
    list_filter = ("is_approved", "request_date")


@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ("loan", "amount", "payment_date_jalali", "is_approved")
    list_filter = ("is_approved", "payment_date")
