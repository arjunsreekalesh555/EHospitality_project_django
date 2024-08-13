from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from patient_app.forms import *
from patient_app.forms import DoctorForm
from patient_app.models import Patient, MedicalHistory, Appointment, Doctor
from .forms import *

#create your views here
#help page
def help(request):

    return render(request, 'doctor/help.html')

#doctor home page
def doctor_home(request):
    if not request.user.is_authenticated:
        return redirect('doctor_register')

    try:
        doctor = request.user.doctor
    except ObjectDoesNotExist:
        messages.error(request, "Invalid credentials or no associated doctor profile found.", extra_tags='error_login')
        return redirect('doctor_login')


    appointments = Appointment.objects.filter(doctor=doctor, status='Accepted')
    ap_count=appointments.count()
    return render(request, 'doctor/home.html', {'ap_count':ap_count})

#doctor register
def doctor_register(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('password2')
        doctor = request.POST.get('doctor')
        specialization_id = request.POST.get('special')
        mobile = request.POST.get('mobile')
        qualification = request.POST.get('qualification')
        image = request.FILES.get('image')
        experience = request.POST.get('experience')
        hospital = request.POST.get('hospital')
        gender = request.POST.get('gender')
        language = request.POST.get('language')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists', extra_tags='username_exists')
                return redirect('doctor_register')
            else:
                user = User.objects.create_user(username=username, password=password)
                specialization = Department.objects.get(id=specialization_id)

                Doctor.objects.create(
                    user=user,
                    doctor=doctor,
                    mobile=mobile,
                    experience=experience,
                    hospital=hospital,
                    gender=gender,
                    specialization=specialization,
                    qualification=qualification,
                    image=image,
                    language=language,
                )
                messages.success(request, 'Registration successful. You can now login.', extra_tags='success_register')
                return redirect('doctor_login')
        else:
            messages.info(request, 'Passwords do not match', extra_tags='password_mismatch')
            return redirect('doctor_register')

    return render(request, 'doctor/doctor_register.html', {'departments': departments})

#doctor login
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Doctor logged in successfully!', extra_tags='success_login')
            return redirect('doctor_home')
        else:
            messages.info(request, 'Please provide correct details', extra_tags='error_login')
            return redirect('doctor_login')

    return render(request, 'doctor/doctor_login.html')

#edit doctor
def edit_doctor_details(request):
    user = request.user
    try:
        doctor_instance = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        doctor_instance = None

    departments = Department.objects.all()

    if request.method == 'POST':
        doctor_name = request.POST.get('doctor')
        mobile = request.POST.get('mobile')
        qualification = request.POST.get('qualification')
        specialization_id = request.POST.get('special')
        image = request.FILES.get('image')  # Get the uploaded image file
        experience = request.POST.get('experience')
        hospital = request.POST.get('hospital')
        gender = request.POST.get('gender')
        language = request.POST.get('language')

        if doctor_instance:
            doctor_instance.doctor = doctor_name
            doctor_instance.mobile = mobile
            doctor_instance.specialization_id = specialization_id
            doctor_instance.qualification = qualification
            doctor_instance.experience = experience
            doctor_instance.hospital = hospital
            doctor_instance.gender = gender
            doctor_instance.language = language


            if image:
                doctor_instance.image = image

            doctor_instance.save()

        messages.success(request, 'Details updated successfully', extra_tags='update')
        return redirect('logged_doctor_details')

    return render(request, 'doctor/edit_doctor_details.html', {
        'doctor': doctor_instance,
        'departments': departments
    })

#doctor logout
def doctor_logout(request):
    auth.logout(request)
    return redirect('doctor_login')

#add health resource doctor
def add_health_resource_doctor(request):
    if request.method == 'POST':
        form = HealthResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health resource added successfully!', extra_tags='added')
            return redirect('doctor_health_resource_details')
    else:
        form = HealthResourceForm()

    return render(request, 'doctor/add_health_resource_doctor.html', {'form': form})

#edit_health_resource_doctor
def edit_health_resource_doctor(request, resource_id):
    resources=HealthResource.objects.get(id=resource_id)

    if request.method=='POST':
        form=HealthResourceForm(request.POST, instance=resources)

        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully!', extra_tags='updated')
            return redirect('doctor_health_resource_details')

    else:
        form=HealthResourceForm(instance=resources)

    return render(request, 'doctor/edit_health_resource.html', {'form':form})

#health resources details
def doctor_health_resource_details(request):
    resources=HealthResource.objects.all()

    return render(request, 'doctor/doctor_health_resource_details.html', {'resources':resources})

#doctor_appointments
def doctor_appointments(request):
    doctor = request.user.doctor

    appointments = Appointment.objects.filter(doctor=doctor, status='Accepted')
    ap_count=appointments.count()

    return render(request, 'doctor/appointmented.html', {'appointments': appointments, 'ap_count':ap_count})

#appointments_per_doctor
def appointments_per_doctor(request):
    doctor = request.user.doctor

    appointments = Appointment.objects.filter(doctor=doctor, status='Accepted')
    appointments_count=appointments.count()
    return render(request, 'doctor/home.html', {'appointments': appointments, 'appointments_count':appointments_count})

#add_prescription
def add_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = Doctor.objects.get(user=request.user)
            prescription.save()
            messages.success(request, 'Prescription added successfully!', extra_tags='add')
            return redirect('add_prescriptions')
    else:
        form = PrescriptionForm()
    return render(request, 'doctor/add_prescription.html', {'form': form})

#add_treatment_plan
def add_treatment_plan(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        patient = Patient.objects.get(user=appointment.user)
    except Patient.DoesNotExist:
        messages.error(request, 'Patient not found.')
        return redirect('doctor_appointments')
    doctor = get_object_or_404(Doctor, user=request.user)


    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            treatment_plan = form.save(commit=False)
            treatment_plan.patient = patient
            treatment_plan.doctor=doctor
            treatment_plan.save()
            messages.success(request, 'Treatment plan added successfully', extra_tags='added_treatment_plan')
            return redirect('doctor_appointmented')
    else:
        form = MedicalHistoryForm()

    return render(request, 'doctor/add_treatment_plan.html', {'form': form, 'patient': patient})

#logged_doctor_details
def logged_doctor_details(request):
    if request.user.is_authenticated:
        try:
            details=Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            details = None
        return render(request, 'doctor/doctor_details.html', {'details': details})
    else:
        return redirect('doctor_login')

#add_health_resource_doctor
def add_health_resource_doctor(request):
    if request.method == 'POST':
        form = HealthResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_health_resource_doctor')
    else:
        form = HealthResourceForm()

    return render(request, 'doctor/add_health_resource_doctor.html', {'form': form})
