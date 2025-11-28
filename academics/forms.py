from django import forms
from .models import BookOrder

class BookOrderForm(forms.ModelForm):
    class Meta:
        model = BookOrder
        fields = ['student_name', 'student_class', 'parent_name', 'parent_mobile', 'parent_email', 'reason', 'other_reason_details']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Full Name'}),
            'student_class': forms.Select(attrs={'class': 'form-select'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Name'}),
            'parent_mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'parent_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'reason': forms.Select(attrs={'class': 'form-select', 'id': 'reasonDropdown'}), # ID for JS
            'other_reason_details': forms.TextInput(attrs={'class': 'form-control', 'id': 'otherReasonField', 'style': 'display:none;', 'placeholder': 'Please specify other reason'}),
        }