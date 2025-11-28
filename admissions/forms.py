
from django import forms
from .models import ApplicationSubmission

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = ApplicationSubmission
        fields = [
            "child_first_name", "child_last_name", "dob", "gender",
            "parent_name", "email", "phone", "address", "notes"
        ]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "child_first_name": forms.TextInput(attrs={"class": "form-control"}),
            "child_last_name": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "parent_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Any medical conditions or additional info..."}),
        }