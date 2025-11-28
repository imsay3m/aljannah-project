
from django import forms
from .models import BookOrder

class BookOrderForm(forms.ModelForm):
    # Categorized Choices based on your image
    BOOK_CHOICES = [
        ('General Items', (
            ('Homework Diary (£4.00)', 'Homework Diary (£4.00)'),
            ('Dua, Salah & Hifz Book (£11.00)', 'Dua, Salah & Hifz Book (£11.00)'),
        )),
        ('Islamic Class', (
            ('WLS IS Book K (£17.00)', 'WLS IS Book K (£17.00)'),
            ('WLS IS Book 1 (£17.00)', 'WLS IS Book 1 (£17.00)'),
            ('WLS IS Book 2 (£17.00)', 'WLS IS Book 2 (£17.00)'),
            ('WLS IS Book 3 (£17.00)', 'WLS IS Book 3 (£17.00)'),
            ('WLS IS Book 4 (£17.00)', 'WLS IS Book 4 (£17.00)'),
            ('WLS IS Book 5 (£17.00)', 'WLS IS Book 5 (£17.00)'),
            ('WLS IS Book 6 (£17.00)', 'WLS IS Book 6 (£17.00)'),
            ('WLS IS Book 7 (£17.00)', 'WLS IS Book 7 (£17.00)'),
        )),
        ('Quran Class', (
            ('Ahsanul Qawaid (£4.00)', 'Ahsanul Qawaid (£4.00)'),
            ('Juz Amma (£4.00)', 'Juz Amma (£4.00)'),
            ('Own Quran (No Cost)', 'Own Quran'),
        )),
        ('Arabic Class', (
            ('Arabic Alphabet - Letters (£8.00)', 'Arabic Alphabet - Letters (£8.00)'),
            ('Arabic Alphabet - Begin, Mid, End (£8.00)', 'Arabic Alphabet - Begin, Mid, End (£8.00)'),
            ('Arabic Alphabet - Punctuation (£11.00)', 'Arabic Alphabet - Punctuation (£11.00)'),
            ('Arabic Alphabet - Words (FREE)', 'Arabic Alphabet - Words (FREE)'),
            ('Juz Amma Book 1 (£8.00)', 'Juz Amma Book 1 (£8.00)'),
            ('Juz Amma Book 2 (£8.00)', 'Juz Amma Book 2 (£8.00)'),
            ('Juz Amma Book 3 (£8.00)', 'Juz Amma Book 3 (£8.00)'),
            ('Juz Amma Book 4 (£11.00)', 'Juz Amma Book 4 (£11.00)'),
            ('Surah Kahf & Ayatul Kursi Book 5 (£8.00)', 'Surah Kahf & Ayatul Kursi Book 5 (£8.00)'),
        )),
    ]

    # Define field explicitly to use CheckboxSelectMultiple
    selected_books_list = forms.MultipleChoiceField(
        choices=BOOK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Missing Books"
    )

    class Meta:
        model = BookOrder
        fields = ['student_name', 'student_class', 'parent_name', 'parent_mobile', 'parent_email', 'reason', 'other_reason_details', 'selected_books']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Full Name'}),
            'student_class': forms.Select(attrs={'class': 'form-select'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Name'}),
            'parent_mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'parent_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'reason': forms.Select(attrs={'class': 'form-select', 'id': 'reasonDropdown'}),
            'other_reason_details': forms.TextInput(attrs={'class': 'form-control', 'id': 'otherReasonField', 'style': 'display:none;', 'placeholder': 'Please specify other reason'}),
            # selected_books is hidden because we fill it via clean()
            'selected_books': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        reason = cleaned_data.get("reason")
        books_list = cleaned_data.get("selected_books_list")

        # Logic: If reason is 'missing', convert list to string and save
        if reason == 'missing' and books_list:
            cleaned_data['selected_books'] = ", ".join(books_list)
        else:
            cleaned_data['selected_books'] = ""
        
        return cleaned_data