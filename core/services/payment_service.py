from payments.models import Payment
from core.services.balance_service import update_user_balance


def approve_payment(payment_id):
    payment = Payment.objects.get(id=payment_id)
    payment.payment_status = 'A'
    payment.save()
    update_user_balance(payment.user)
