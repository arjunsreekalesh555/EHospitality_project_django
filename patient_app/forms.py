from django import forms
from .models import Patient, Doctor, Appointment, MedicalHistory, Billing, HealthResource, Department, Prescription


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient', 'date_of_birth', 'age', 'phone', 'email', 'gender', 'address']

class DoctorForm(forms.ModelForm):
    specialization = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = Doctor
        fields = ['doctor', 'mobile', 'specialization', 'image', 'qualification', 'gender', 'experience', 'language', 'hospital']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicine']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'department', 'problem', 'date']

class ListAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['problem', 'date']

class UserAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['problem', 'date']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department']

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'medications', 'allergies', 'treatment_history']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'treatment_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'amount_due', 'due_date', 'status']

class HealthResourceForm(forms.ModelForm):
    class Meta:
        model = HealthResource
        fields = ['title', 'content']
