from django.views.generic import FormView, ListView


class RequestLoanView(FormView):
    # todo: user can request loan if register join_date > 4 month
    pass


class ListRequestLoanView(ListView):
    # todo: only admin can access this view to accept or reject loans requests
    pass
