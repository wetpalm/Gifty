from django import forms
from .models import Partner


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = "__all__"

        widget = {
            'name': forms.TextInput(attrs={'class':'form-control', 'style':'margin-bottom:10px'}),
            'category': forms.Select(attrs={'class':'form-select', 'style':'margin-bottom:10px'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'style':'margin-bottom:10px'}),
            'lstate': forms.Select(attrs={'class':'form-select', 'style':'margin-bottom:10px'}),

        }