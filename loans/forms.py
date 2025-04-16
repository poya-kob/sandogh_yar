from django import forms
from .models import LoanRequest


class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['amount']
        labels = {
            'amount': 'مبلغ وام (تومان)',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 5000000'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        user = self.initial.get('user') or self.instance.user
        if LoanRequest.objects.filter(user=user, request_status='A').exists():
            raise forms.ValidationError("شما یک وام فعال دارید.")
        return cleaned_data
