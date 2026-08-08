from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["full_name", "email", "phone", "unit_type", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+254 7XX XXX XXX"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us what you are looking for..."}),
        }
