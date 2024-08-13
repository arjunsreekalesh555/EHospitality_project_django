from django.urls import path, include
from . import views

urlpatterns=[
    path('help-page/', views.help, name='help'),
    path('doctor-home/', views.doctor_home, name='doctor_home'),
    path('doctor-register/', views.doctor_register, name='doctor_register'),
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('edit_doctor/', views.edit_doctor_details, name='edit_doctor'),
    path('doctor-logout/', views.doctor_logout, name='doctor_logout'),
    path('doctor-health-resource-details/', views.doctor_health_resource_details, name='doctor_health_resource_details'),
    path('edit-health-resources-doctor/<int:resource_id>/', views.edit_health_resource_doctor, name='edit_health_resource_doctor'),
    path('doctor-appointmentd/', views.doctor_appointments, name='doctor_appointmented'),
    path('appointment-count/', views.appointments_per_doctor, name='appointments_count'),
    path('doctor-add-treatment-plan/<int:appointment_id>/', views.add_treatment_plan, name='add_treatment_plan'),
    path('doctor/add_prescription/', views.add_prescription, name='add_prescriptions'),
    path('doctor-details/', views.logged_doctor_details, name='logged_doctor_details'),
    path('add-health-resource-doctor/', views.add_health_resource_doctor, name='add_health_resource_doctor'),
]
