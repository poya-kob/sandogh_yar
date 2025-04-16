from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'receipt_image', 'payment_date']
        labels = {
            'amount': 'مبلغ فیش واریزی (تومان)',
            'receipt_image': 'تصویر فیش واریزی',
            'payment_date': 'تاریخ پرداخت',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 5000000'}),
            'receipt_image': forms.ImageField(),
            'payment_date': forms.DateInput(),  # todo: make widgets compatible with jalali calender
        }
