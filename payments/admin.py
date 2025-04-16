from django.contrib import admin
from .models import MembershipFee, Payment, BalanceSheet


@admin.register(MembershipFee)
class MembershipFeeAdmin(admin.ModelAdmin):
    list_display = ("amount", "start_date", "end_date")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "payment_date", "is_approved")
    list_filter = ("is_approved", "payment_date")


@admin.register(BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = ("user", "total_paid", "remaining_balance")
