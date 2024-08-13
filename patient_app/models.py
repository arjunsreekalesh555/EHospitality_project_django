from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.CharField(max_length=250)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.patient

class Department(models.Model):
    department=models.CharField(max_length=100)

    def __str__(self):
        return self.department

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    doctor = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15)
    specialization = models.ForeignKey(Department, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    qualification = models.CharField(max_length=256)
    experience=models.CharField(max_length=256)
    hospital=models.CharField(max_length=256)
    gender=models.CharField(max_length=10)
    language=models.CharField(max_length=10)

    def __str__(self):
        return self.doctor

class Prescription(models.Model):
    doctor=models.ForeignKey('Doctor', on_delete=models.CASCADE)
    medicine=models.CharField(max_length=200)

    def __str__(self):
        return self.medicine

class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    STATUS_CHOICE = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICE)
    payment_time = models.DateTimeField(null=True, blank=True)
    is_new = models.BooleanField(default=True)
    def __str__(self):
        return f"Billing for {self.patient.patient}"

    def is_paid(self):
        return self.status == 'Paid'


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this field
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    problem = models.TextField()
    date = models.DateTimeField()
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    accepted = models.BooleanField(default=False)
    billing = models.OneToOneField(Billing, on_delete=models.CASCADE, null=True, blank=True)

    received_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment with {self.doctor.doctor} for {self.patient.patient} on {self.date}"

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medications = models.TextField()
    allergies = models.TextField()
    treatment_history = models.TextField()

    received_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.user.username} - {self.diagnosis}"

class HealthResource(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
