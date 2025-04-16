from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from persiantools.jdatetime import JalaliDate

from .models import LoanRequest, InstallmentSchedule
from .forms import LoanRequestForm
from .mixins import NoActiveLoanMixin


class RequestLoanView(NoActiveLoanMixin, FormView):
    # todo: user can request loan if register join_date > 4 month
    form_class = LoanRequestForm

    def get_template_names(self):
        user_signup_gregorian = self.request.user.date_joined.date()
        user_signup_jalali = JalaliDate(user_signup_gregorian)
        now_jalali = JalaliDate.today()

        # اختلاف ماه و سال رو محاسبه می‌کنیم
        total_months = (now_jalali.year - user_signup_jalali.year) * 12 + (now_jalali.month - user_signup_jalali.month)

        if total_months >= 4:
            return ['loans/create_request.html']
        return ['loans/not_eligible.html']

    def form_valid(self, form):
        loan_request = form.save(commit=False)
        loan_request.user = self.request.user  # کاربر جاری
        loan_request.save()
        messages.success(self.request, "درخواست شما با موفقیت ثبت شد.")
        return self.render_to_response(self.get_context_data(form=self.form_class()))  # فرم خالی برمی‌گرده

    def form_invalid(self, form):
        messages.error(self.request, "خطا در ثبت فرم. لطفاً ورودی‌ها را بررسی کنید.")
        return super().form_invalid(form)


class ListRequestLoanView(UserPassesTestMixin, ListView):
    # todo: only admin can access this view to accept or reject loans requests
    model = LoanRequest
    template_name = 'loans/loan_request_list.html'
    context_object_name = 'loan_requests'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status in dict(LoanRequest.STATUS_CHOICES):
            queryset = queryset.filter(request_status=status)
        return queryset


class ListUsersInstallments(ListView):
    # todo: users can see remaining installments here
    model = InstallmentSchedule
    template_name = 'loans/user_installments.html'
    context_object_name = 'installments'

    def get_queryset(self):
        queryset = InstallmentSchedule.objects.filter(
            loan__user=self.request.user,
            loan__request_status='A'  # فقط وام‌های تایید شده
        ).order_by('due_date')
        status = self.request.GET.get('status')
        if status in dict(LoanRequest.STATUS_CHOICES):
            queryset = queryset.filter(request_status=status)
        return queryset
