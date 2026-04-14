from django import forms
from .models import Appointment
import datetime


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'student_name', 'student_id', 'email', 'contact',
            'office', 'date', 'time', 'purpose', 'notes'
        ]
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. John Martin',
                'autocomplete': 'name',
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. 2312103 (optional)',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. martin@gmail.com',
                'autocomplete': 'email',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. 09XX-XXX-XXXX',
            }),
            'office': forms.Select(attrs={
                'class': 'form-input form-select',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time',
            }),
            'purpose': forms.Select(attrs={
                'class': 'form-input form-select',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Any additional details or special requests...',
                'rows': 3,
            }),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < datetime.date.today():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        if date and date.weekday() >= 5:
            raise forms.ValidationError("Appointments are only available Monday to Friday.")
        return date

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        digits = ''.join(filter(str.isdigit, contact))
        if len(digits) < 10:
            raise forms.ValidationError("Please enter a valid contact number (at least 10 digits).")
        return contact

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time:
            office_open = datetime.time(8, 0)
            office_close = datetime.time(17, 0)
            if not (office_open <= time <= office_close):
                raise forms.ValidationError("Appointment time must be between 8:00 AM and 5:00 PM.")
        return time


class AppointmentSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Search by name, ID, or purpose...',
        })
    )
    office = forms.ChoiceField(
        required=False,
        choices=[('', 'All Offices')] + Appointment.OFFICE_CHOICES,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + Appointment.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    date_filter = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'filter-select',
            'type': 'date',
        })
    )
