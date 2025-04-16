from django.views.generic import FormView
from django.contrib import messages

from .forms import PaymentForm


class MembershipFeeView(FormView):
    # todo: create new MembershipFee record only admin can access this page
    pass


class MembershipFeePaymentView(FormView):
    # todo: users upload payment bill
    form_class = PaymentForm

    def form_valid(self, form):
        loan_request = form.save(commit=False)
        loan_request.user = self.request.user  # کاربر جاری
        loan_request.save()
        messages.success(self.request, "درخواست شما با موفقیت ثبت شد.")
        return self.render_to_response(self.get_context_data(form=self.form_class()))  # فرم خالی برمی‌گرده
