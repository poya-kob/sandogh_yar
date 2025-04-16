from django.views.generic import FormView


class MembershipFeeView(FormView):
    # todo: create new MembershipFee record only admin can access this page
    pass


class MembershipFeePaymentView(FormView):
    # todo: users upload payment bill
    pass
