import stripe as stripe
from datetime import date
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import stripe
from patient_app.forms import AppointmentForm, PatientForm, MedicalHistoryForm, BillingForm, UserAppointmentForm, ListAppointmentForm
from patient_app.models import Patient, Doctor, MedicalHistory, Appointment, Department, Billing, HealthResource
import logging

# Create your views here.
#about us page
def about_us(request):
    patient = Patient.objects.get(user=request.user)
    context = {
        'patient': patient,
    }
    return render(request, 'user/about_us.html', context)

#hel page
def help(request):

    return render(request, 'user/help.html')


#user logout
def user_logout(request):
    auth.logout(request)
    return redirect('user_login')

#main page
def user_home(request):
    user = request.user
    try:
        patient = Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        patient = None

    if not request.user.is_authenticated:
        return redirect('user_register')

    doctors=Doctor.objects.all()
    dcounts=doctors.count()


    context={
        'doctors':doctors, 'dcounts':dcounts,
        'patient':patient

    }

    return render(request, 'user/user_home.html', context)

#doctor list
def doctor_list(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    doctors=Doctor.objects.all()

    return render(request, 'user/doctor_list.html', {'doctors':doctors})

#booking appointments
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.save()
            return redirect('user_appointment_details', appointment_id=appointment.id)  # Redirect to a success page
    else:
        form = AppointmentForm()

    return render(request, 'user/book_appointment.html', {'form': form, 'doctor': doctor})

#appointment details
def user_appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    return render(request, 'user/appointment_details.html', {'appointment': appointment})

#user register
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('password2')
        name = request.POST.get('name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!', extra_tags='username_exists')
                return redirect('user_register')
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
                user.save()

                # Create an associated Patient record
                Patient.objects.create(
                    user=user,
                    patient=name,
                    date_of_birth=date_of_birth,
                    age=age,
                    gender=gender,
                    email=email,
                    address=address,
                    phone=mobile
                )
                messages.success(request, 'Registration successful. You can now login.', extra_tags='success_register')
                return redirect('user_login')
        else:
            messages.error(request, 'Passwords do not match', extra_tags='password_mismatch')
            return redirect('user_register')

    return render(request, 'user/register.html')

#user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful..', extra_tags='success_login')
            return redirect('user_home')
        else:
            messages.info(request, 'Invalid credentials!', extra_tags='error_login')
            return redirect('user_login')

    return render(request, 'user/login.html')

#edit user details
def edit_user_details(request):
    user = request.user
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

        messages.success(request, 'Details updated successfully', extra_tags='update')
        return redirect('user_details')

    return render(request, 'user/edit_user_details.html', {'patient': patient})

#logged user details
def user_details(request):
    if request.user.is_authenticated:
        try:
            details=Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            details = None
        patient = Patient.objects.get(user=request.user)
        context = {
            'patient': patient,
            'details': details,
        }

        return render(request, 'user/patient_details.html', context)
    else:
        return redirect('user_login')

#doctor details
def doctor_details_user(request):
    if request.user.is_authenticated:
        try:
            details=Doctor.objects.all()
        except Doctor.DoesNotExist:
            details = None
        patient = Patient.objects.get(user=request.user)
        context = {
            'patient': patient,
            'details': details,
        }

        return render(request, 'user/doctor_details_user.html', context)
    else:
        return redirect('user_login')

#doctor details in list
def doctor_details_list(request):
    if request.user.is_authenticated:
        details = Doctor.objects.all()

        paginator = Paginator(details, 5)
        page_number = request.GET.get('page')

        try:
            page = paginator.get_page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        patient = Patient.objects.get(user=request.user)
        context = {
            'patient': patient,
            'details': page,
        }
        return render(request, 'user/doctor_details_list.html', context)
    else:
        return redirect('user_login')

#book appointment
def doctor_list_and_book_appointment(request):
    doctors = Doctor.objects.all()
    departments = Department.objects.all()
    patient = Patient.objects.get(user=request.user)


    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        department_id = request.POST.get('department')
        department = get_object_or_404(Department, id=department_id)
        problem = request.POST.get('problem')
        date = request.POST.get('date')

        doctor = get_object_or_404(Doctor, id=doctor_id)

        appointment = Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            department=department,
            problem=problem,
            date=date,
            status='Pending'
        )

        messages.success(request, 'Appointment booked successfully!', extra_tags='success')
        return redirect('user_appointment_list')

    return render(request, 'user/doctor_list_and_book_appointment.html', {'doctors':doctors, 'departments':departments, 'patient':patient})

#delete appointment
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully', extra_tags='delete')
        return redirect('user_appointment_list')
    return render(request, 'user/delete_appointment.html', {'appointment': appointment})

#user reschedule appointment
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    patient = Patient.objects.get(user=request.user)

    if request.method == 'POST':
        form = ListAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully', extra_tags='update')
            return redirect('user_appointment_list')
    else:
        form = ListAppointmentForm(instance=appointment)
    return render(request, 'user/update_appointment.html', {'form': form, 'patient':patient})

#appointment list user
def user_appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    patient = Patient.objects.get(user=request.user)

    return render(request, 'user/appointment_list.html', {'appointments': appointments, 'patient':patient})

#patients treatment plan
def patient_treatment_plan(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    treatment_plans = MedicalHistory.objects.filter(patient=patient)
    current_datetime = timezone.now()

    return render(request, 'user/treatment_plan.html', {'patient': patient, 'treatment_plans': treatment_plans, 'current_datetime':current_datetime})

#checkout
def createCheckout(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY

        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)

        try:
            patient = Patient.objects.get(user=appointment.user)
        except Patient.DoesNotExist:
            return HttpResponse("Patient record not found", status=404)

        billing = Billing.objects.create(
            patient=patient,
            amount_due=200,
            user=request.user,
            due_date=date.today(),
            status='Unpaid'
        )
        appointment.billing = billing
        appointment.save()

        lineitems = [{
            'price_data': {
                'currency': 'INR',
                'unit_amount': 20000,
                'product_data': {
                    'name': f"Appointment with Dr. {appointment.doctor.doctor}"
                },
            },
            'quantity': 1,
        }]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=lineitems,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')) + f"?appointment_id={appointment.id}",
            cancel_url=request.build_absolute_uri(reverse('cancel')),
        )

        return redirect(checkout_session.url, code=303)

    return HttpResponse("Method not allowed", status=405)

#success
def success(request):
    appointment_id = request.GET.get('appointment_id')
    if appointment_id:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        if appointment.billing:
            appointment.billing.status = 'Paid'
            appointment.billing.payment_time = timezone.now()
            appointment.billing.save()
            messages.success(request, 'Payment successfull!', extra_tags='success_payment')
    return render(request, 'user/success.html')

#cancelled
def cancel(request):
    messages.success(request, 'Payment cancelled!', extra_tags='cancel_payment')
    return render(request, 'user/cancel.html')

#user health resource
def user_health_resource_details(request):
    resources=HealthResource.objects.all()
    patient = Patient.objects.get(user=request.user)

    paginator = Paginator(resources, 7)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'user/user_health_resource_details.html', {'resources':page, 'patient':patient})

#register user
def register_user(request):
    return render(request, 'user/register.html')

#appoint doctor from doctor list
def appoint_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    department = doctor.specialization
    patient = Patient.objects.get(user=request.user)

    if request.method == 'POST':
        form = ListAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.department = department
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Appointed successfully!')
            return redirect('user_appointment_list')
        else:
            print(form.errors)
            messages.error(request, 'There was an error with your appointment. Please try again.', extra_tags='error')
    else:
        form = ListAppointmentForm()
    context = {
        'form': form,
        'doctor': doctor,
        'department': department,
        'patient':patient
    }
    return render(request, 'user/appoint_doctor.html', context)

#search_doctor_from_list
def search_doctor_from_list(request):
    query = request.GET.get('q', None)
    doctors = Doctor.objects.filter(Q(doctor__icontains=query) | Q(hospital__icontains=query) |Q(language__icontains=query) | Q(gender__icontains=query)) if query else Doctor.objects.all()
    patient = Patient.objects.get(user=request.user)

    return render(request, 'user/search_doctor_from_list.html', {'doctors': doctors, 'query': query, 'patient':patient})

#search doctor
def search_doctors(request):
    query = request.GET.get('q', None)
    doctors = Doctor.objects.filter(Q(doctor__icontains=query) | Q(hospital__icontains=query) |Q(language__icontains=query) | Q(gender__icontains=query)) if query else Doctor.objects.all()
    patient = Patient.objects.get(user=request.user)

    return render(request, 'user/search_doctors.html', {'doctors': doctors, 'query': query, 'patient':patient})

def payment_history(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = None

    if patient:
        billing_records = Billing.objects.filter(patient=patient).order_by('-due_date')
    else:
        billing_records = []

    return render(request, 'user/view_payments.html', {'billing_records': billing_records})
