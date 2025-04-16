from django.contrib import messages
from django.shortcuts import redirect
from loans.models import LoanRequest


class NoActiveLoanMixin:
    def dispatch(self, request, *args, **kwargs):
        has_active_loan = LoanRequest.objects.filter(
            user=request.user,
            request_status='A'  # وام تایید شده
        ).exists()

        if has_active_loan:
            messages.error(request, "شما یک وام تاییدشده دارید و نمی‌توانید درخواست جدید ثبت کنید.")
            return redirect("home")  # یا هر جایی که مناسب باش  todo:change redirect

        return super().dispatch(request, *args, **kwargs)
