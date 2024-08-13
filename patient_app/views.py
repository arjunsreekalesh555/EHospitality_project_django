from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from django.contrib import messages, auth
from .forms import *
from .models import *
from django.contrib.auth.models import User
from doctor_app.models import*
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.utils import timezone


# Create your views here.
#main page
def main(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    patients=Patient.objects.all()
    pcounts=patients.count()
    doctors=Doctor.objects.all()
    dcounts=doctors.count()
    appointments=Appointment.objects.all()
    acounts = appointments.count()

    pending_appointments_count = Appointment.objects.filter(status__in=['Pending', '']).count()

    context={
        'patients': patients,'pcounts': pcounts,
        'doctors':doctors, 'dcounts':dcounts,
        'appointments':appointments, 'acounts':acounts,
        'pending_appointments_count': pending_appointments_count

    }

    return render(request, 'admin/index.html', context)


#add patient
def add_patient(request):
    if request.method=='POST':
        form=PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add_patient')
    else:
        form=PatientForm()


    return render(request, 'admin/add_patient.html', {'form':form})

#patient details
def pat_details(request):
    pdetails=Patient.objects.all()

    return render(request, 'admin/pat.html', {'pdetails':pdetails})


#delete patient
def delete_patient(request, pat_id):
    error=''

    detail = get_object_or_404(Patient, id=pat_id)

    if request.method=='POST':

        try:
            detail.delete()
            error='no'
            return redirect('pat_details')

        except:
            error='yes'

    context={'error':error, 'detail':detail}

    return render(request, 'admin/delete_patient.html', context)

#add patients medical history
def add_medical_history(request):
    details=MedicalHistory.objects.all()
    if request.method=='POST':
        form=MedicalHistoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add_medical_history')
    else:
        form=MedicalHistoryForm()

    return render(request, 'admin/add_medical_history.html', {'form':form, 'details':details})

#medical history details
def medical_history_details(request):
    details=MedicalHistory.objects.all()

    return render(request, 'admin/medical_history_details.html', {'details':details})

#delete medical history details
def delete_medical_history(request, history_id):
    error=''

    detail=get_object_or_404(Patient, id=history_id)

    if request.method=='POST':

        try:
            detail.delete()
            error='no'
            return redirect('medical_history_details')

        except:
            error='yes'

    context={'error':error, 'detail':detail}

    return render(request, 'admin/delete_medical_history.html', context)

#delete appointment
def delete_appointment(request, appoint_id):
    error=''

    detail = get_object_or_404(Patient, id=appoint_id)

    if request.method=='POST':

        try:
            detail.delete()
            error='no'
            return redirect('appointment_details')

        except:
            error='yes'

    context={'error':error, 'detail':detail}

    return render(request, 'admin/delete_appointment.html', context)

#delete payment
def delete_payment(request, payment_id):
    error=''

    detail = get_object_or_404(Billing, id=payment_id)

    if request.method=='POST':

        try:
            detail.delete()
            error='no'
            return redirect('payment_details')

        except:
            error='yes'

    context={'error':error, 'detail':detail}

    return render(request, 'admin/delete_payment.html', context)


#add appointment
def add_appointment(request):
    appointment_details=Appointment.objects.all()
    if request.method=='POST':
        form=AppointmentForm(request.POST)

        if form.is_valid():
            form.save()
            print('Form', form)
            return redirect('add_appointment')
    else:
        form=AppointmentForm()

    return render(request, 'admin/add_appointment.html', {'form':form, 'appointment_details':appointment_details})

#appointment details
def appointment_details(request):
    details=Appointment.objects.all()

    return render(request, 'admin/appointment_details.html', {'details':details})

#add payment
def add_payment(request):
    billing_details=Billing.objects.all()
    if request.method=='POST':
        form=BillingForm(request.POST)

        if form.is_valid():
            form.save()
            print('Form', form)
            return redirect('add_payment')
    else:
        form=BillingForm()

    return render(request, 'admin/add_payment.html', {'form':form, 'billing_details':billing_details})

#payment details
def payment_details(request):
    details=Billing.objects.all()

    return render(request, 'admin/payment_details.html', {'details':details})

#add health resource
def add_health_resource(request):
    if request.method == 'POST':
        form = HealthResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health resource added successfully!', extra_tags='add')
            return redirect('add_health_resource')
    else:
        form = HealthResourceForm()

    return render(request, 'admin/admin_add_health_resources.html', {'form': form})

def edit_health_resource(request, resource_id):
    resources=HealthResource.objects.get(id=resource_id)

    if request.method=='POST':
        form=HealthResourceForm(request.POST, instance=resources)

        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully!', extra_tags='update')
            return redirect('health_resource_details')


    else:
        form=HealthResourceForm(instance=resources)

    return render(request, 'admin/admin_edit_health_resources.html', {'form':form})

#health resources details
def health_resource_details(request):
    resources=HealthResource.objects.all()

    return render(request, 'admin/health_resource_details.html', {'resources':resources})

#search doctors
def search_doctor(request):
    query=None
    doctors=None
    patients=None

    if 'q' in request.GET:
        query=request.GET.get('q')
        doctors=Doctor.objects.filter(Q(doctor__icontains=query))
        patients=Patient.objects.filter(Q(patient__icontains=query))

    else:
        doctors=[]

    return render(request, 'admin/search_doctors.html', {'doctors': doctors, 'patients':patients, 'query': query})

#admin_login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'please provide correct details')
            return redirect('admin_login')

    return render(request, 'admin/admin_login.html')

#admin_logout
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')

#add_department
def add_department(request):
    details=Department.objects.all()

    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully.', extra_tags='add')
            return redirect('add_department')
    else:
        form=DepartmentForm()

    return render(request, 'admin/add_department.html', {'form': form, 'details':details})

#add department
def department_list(request):
    details=Department.objects.all()

    return render(request, 'admin/department_list.html', {'details': details})

#delete department
def delete_department(request, department_id):
    departments=Department.objects.get(id=department_id)
    if request.method=='POST':
        departments.delete()
        messages.success(request, 'Department deleted successfully.', extra_tags='delete')

        return redirect('add_department')

    return render(request, 'admin/delete_department.html', {'departments':departments})

#doctor details
def doctor_details(request):
    if request.user.is_authenticated:
        details=Doctor.objects.all()
        paginator = Paginator(details, 5)  # Show 6 doctors per page
        page_number = request.GET.get('page')

        try:
            page = paginator.get_page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return render(request, 'admin/doctor_details.html', {'details': page})
    else:
        return redirect('doctor_login')

#manage appointments
def manage_appointments(request):
    appointments = Appointment.objects.all()
    current_datetime = timezone.now()
    return render(request, 'admin/manage_appointments.html', {'appointments': appointments, 'current_datetime':current_datetime})

#all_appointments_from_start
def all_appointments_from_start(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin/all_appointments.html', {'appointments': appointments})

#accept_appointment
def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.accepted = True
    appointment.status = 'Accepted'
    appointment.save()
    messages.success(request, 'Appointment accepted successfully')
    return redirect('manage_appointments')

#decline_appointment
def decline_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Declined'
    appointment.save()
    messages.success(request, 'Appointment declined')
    return redirect('manage_appointments')

#delete_prescription
def delete_prescription(request, prescription_id):
    prescriptions=Prescription.objects.get(id=prescription_id)
    if request.method=='POST':
        prescriptions.delete()

        return redirect('view_prescriptions')

    return render(request, 'admin/delete_prescription.html', {'prescriptions':prescriptions})

#view_prescriptions
def view_prescriptions(request):
    prescriptions = Prescription.objects.all()
    current_date = timezone.now().date()
    return render(request, 'admin/view_prescriptions.html', {'prescriptions': prescriptions, 'current_date': current_date})

#delete_doctor
def delete_doctor(request, doctor_id):
    doctor=Doctor.objects.get(id=doctor_id)
    user = doctor.user
    if request.method=='POST':
        doctor.delete()
        user.delete()
        messages.success(request, "Doctor detail's deleted successfully!", extra_tags='deleted_doctor')
        return redirect('doctor_details')

    return render(request, 'admin/delete_doctor.html', {'doctor':doctor})

#edit user details
def edit_user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        patient = Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        patient = None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        name = request.POST.get('name')
        age = request.POST.get('age')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        if patient:
            patient.patient = name
            patient.age = age
            patient.date_of_birth = date_of_birth
            patient.gender = gender
            patient.address = address
            patient.phone = mobile
            patient.save()

        messages.success(request, 'Patient details updated successfully')
        return redirect('pat_details')

    return render(request, 'admin/edit_user_details.html', {'patient': patient})

#edit_doctor_details
def edit_doctor_details(request, doctor_id):
    doctor_instance = get_object_or_404(Doctor, id=doctor_id)
    departments = Department.objects.all()

    if request.method == 'POST':
        doctor_name = request.POST.get('doctor')
        mobile = request.POST.get('mobile')
        experience = request.POST.get('experience')
        specialization_id = request.POST.get('special')
        qualification = request.POST.get('qualification')
        language = request.POST.get('language')
        gender = request.POST.get('gender')
        hospital = request.POST.get('hospital')


        doctor_instance.doctor = doctor_name
        doctor_instance.mobile = mobile
        doctor_instance.language = language
        doctor_instance.gender = gender
        doctor_instance.hospital = hospital
        doctor_instance.experience = experience
        doctor_instance.qualification = qualification
        doctor_instance.specialization_id = specialization_id
        doctor_instance.save()

        messages.success(request, 'Details updated successfully', extra_tags='updated_doctor_details')
        return redirect('doctor_details')

    return render(request, 'admin/edit_doctor_admin.html', {'doctor': doctor_instance, 'departments': departments})

#search_patients
def search_patients(request):
    query = request.GET.get('q', None)
    patients = Patient.objects.filter(Q(patient__icontains=query) |
                                     Q(email__icontains=query)) if query else Patient.objects.all()

    return render(request, 'admin/search_patients.html', {'patients': patients, 'query': query})

#search_doctor_from_list_admin
def search_doctor_from_list_admin(request):
    query = request.GET.get('q', None)
    doctors = Doctor.objects.filter(Q(doctor__icontains=query) | Q(hospital__icontains=query) |Q(language__icontains=query) | Q(gender__icontains=query)) if query else Doctor.objects.all()
    return render(request, 'admin/search_doctors_admin.html', {'doctors': doctors, 'query': query})

#search_manage_appointments
def search_manage_appointments(request):
    query = request.GET.get('q', None)
    if query:
        details = Appointment.objects.filter(
            Q(doctor__doctor__icontains=query) | Q(user__first_name__icontains=query) | Q(
                user__last_name__icontains=query) | Q(status__icontains=query)
        )
    else:
        details = Appointment.objects.all()

    return render(request, 'admin/search_manage_appointments.html', {'details': details, 'query': query})

def all_payment(request):
    billing_records=Billing.objects.all()

    return render(request, 'admin/all_payments.html', {'billing_records': billing_records})