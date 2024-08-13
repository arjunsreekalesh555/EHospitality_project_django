from django.urls import path, include
from . import views
from .views import manage_appointments, accept_appointment, decline_appointment

from django.contrib import admin

urlpatterns=[
path('admin_home/', views.main, name='home'),
path('patient-logout', views.admin_logout, name='admin_logout'),
path('', views.admin_login, name='admin_login'),
path('add-patient/', views.add_patient, name='add_patient'),
path('add-medical-history/', views.add_medical_history, name='add_medical_history'),
path('medical-history-details/', views.medical_history_details, name='medical_history_details'),
path('delete-medical-details/<int:history_id>', views.delete_medical_history, name='delete_medical_detail'),
path('add-appointment/', views.add_appointment, name='add_appointment'),
path('add-payment/', views.add_payment, name='add_payment'),
path('add-department/', views.add_department, name='add_department'),
path('pat-details', views.pat_details, name='pat_details'),
path('delete-patient/<int:pat_id>/', views.delete_patient, name='delete_patient'),
path('appointment-details/', views.appointment_details, name='appointment_details'),
path('delete-appointment/<int:appoint_id>/', views.delete_appointment, name='delete_appointment'),
path('payment-details/', views.payment_details, name='payment_details'),
path('delete-payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
path('add-health-resource-patient/', views.add_health_resource, name='add_health_resource'),
path('health-resource-details-patient/', views.health_resource_details, name='health_resource_details'),
path('edit-health-resources-patient/<int:resource_id>/', views.edit_health_resource, name='edit_health_resource'),
path('searchfordoctor/', views.search_doctor, name='search_doctor'),
path('doctor-details/', views.doctor_details, name='doctor_details'),
path('dep_list/', views.department_list, name='department_list'),
path('delete-department/<int:department_id>/', views.delete_department, name='delete_department'),
path('appointments/', views.manage_appointments, name='manage_appointments'),
path('all-appointments/', views.all_appointments_from_start, name='all_appointments'),
path('patient-appointments-accept/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
path('patient-appointments-decline/<int:appointment_id>/', views.decline_appointment, name='decline_appointment'),
path('patient-view-prescriptions/', views.view_prescriptions, name='view_prescriptions'),
path('patient-delete-prescriptions/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
path('patient-delete-doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
path('edit_user_details/<int:user_id>/', views.edit_user_details, name='admin_edit_user_details'),
path('edit_doctor/<int:doctor_id>/', views.edit_doctor_details, name='edit_doctor_admin'),
path('appointed-patient-details//', views.search_patients, name='search_patients'),
path('search-doctors/', views.search_doctor_from_list_admin, name='search_doctors_admin'),
path('search-appointments/', views.search_manage_appointments, name='search_manage_appointments'),
path('view-payments/', views.all_payment, name='all_payments'),

]
