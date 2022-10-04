from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm ### Login form
from django.core import exceptions
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.forms import inlineformset_factory

from dent.decorators import unauthenticated_user

from .models import Patient, Staff, Appointment
from .forms import AppointmentForm, CreateUserForm, PatientForm, StaffForm, HOUR_CHOICES
from .filters import AppointmentFilter
from .decorators import unauthenticated_user, allowed_users


#### APPOINTMENTS FILTERING ####
def filter(request):
    appointments = Appointment.objects.all()
    appointfilter = AppointmentFilter(request.GET, queryset=appointments)
    appointments = appointfilter.qs
    filter_list = [appointments, appointfilter, appointments]
    return filter_list


#### CHECK FOR EXISTING APPOINTMENT FOR THE GIVEN DOCTOR, DATE, TIME ####
def appointmentcheck():
    new_appointment = Appointment.objects.last()
    n = 0
    dict_new_appointment = {
        'doctor': new_appointment.doctor.id,
        'date': new_appointment.date,
        'time': new_appointment.time}
    for appoint in Appointment.objects.values('doctor','date','time'):
        if dict_new_appointment == appoint:
            n += 1
    if n >= 2:
        new_appointment.delete()
        return redirect('dent:warning')
    else: 
        return redirect('dent:detail', new_appointment.id )


#### VIEWS  ####

#### HOME PAGE ####
def home(request):
    doctors = Staff.objects.filter(id__range = (2,10))
    id = Staff.objects.filter(id__range = (2,10)).values('id')
    context = {
        'form':doctors,
        'id':id}
    return render(request, 'dent/home.html', context)


#### LOG PATIENT ####
@login_required(login_url = 'dent:login')
@allowed_users(allowed_roles = ['patients'])
def logpatientview(request,pk):
    ''' 
    try refers to that logpatient can update his personal info
    except enables newly logged-in patient to pass in his/her required personal info
        - it takes some personal info from the User`s database table  
    '''
    try:
        current_patient = request.user.patient
        update_patientform = PatientForm(instance = current_patient)
        if request.method == "POST":
            update_patientform = PatientForm(request.POST, instance = current_patient)
            if update_patientform.is_valid():
                update_patientform.save()
                return redirect('dent:logpatientappointment', pk = request.user.patient.id )
        
        ctx = {'patientform':update_patientform}
        return render(request, 'dent/logpatient.html', ctx)

    except:
        saveduser = User.objects.get(id = pk)
        patientform = PatientForm(initial={
            'user':saveduser,
            'fname':saveduser.first_name,
            'sname':saveduser.last_name,
            'email':saveduser.email})
        if request.method == 'POST':
            patientform = PatientForm(request.POST,
            initial={
                'fname':saveduser.first_name,
                'sname':saveduser.last_name,
                'email':saveduser.email,})
            if patientform.is_valid():
                patientform.save()
                new_patient = Patient.objects.last()
                return redirect('dent:logpatientappointment', pk =  new_patient.id )

        ctx = {'patientform':patientform, }
        return render(request, 'dent/logpatient.html', ctx)


@login_required(login_url='dent:login')
@allowed_users(allowed_roles = ['patients'])
def logpatientappointmentview(request,pk):
    ''' 
    try:
        - make an appointment of loged in patient, 
        - check the appointment by appointmentcheck(),
        - throw in the appointment/appointments from database of current loged-in patient
    except redirects the newly logged-in user to logpatient view in order to pass in his/her required personal info  
    '''
    try:
        logpatient = Patient.objects.get(id = pk)
        PatientFormSet = inlineformset_factory(
            Patient, Appointment, 
            fields = ('patient','doctor', 'date', 'time','notes'),
            extra = 1,
            widgets = {
                'doctor':forms.Select(attrs = {'class':'text-input'}),
                'date':forms.DateInput(attrs = {'type':'date', 'class':'text-input'}),
                'time':forms.Select(
                    attrs = {'class':'text-input'},
                    choices = HOUR_CHOICES),
                'notes':forms.Textarea(attrs = {'class':'textarea-input'})},
            can_delete=False)
        formset = PatientFormSet(instance = logpatient, queryset = Appointment.objects.none())
        filter_list = filter(request)
        if request.method == "POST":
            formset = PatientFormSet(request.POST, instance = logpatient)
            if formset.is_valid():
                formset.save()
                return appointmentcheck()

        if Appointment.objects.filter(patient = logpatient.id).exists():
            if Appointment.objects.filter(patient = logpatient.id).count() > 1:
                patientappoints = Appointment.objects.filter(patient = logpatient.id)
                ctx = {
                    'appointments':filter_list[2],
                    'appointfilter':filter_list[1],
                    'patientappoints':patientappoints,
                    'formset':formset,
                    'logpatient':logpatient}
                return render(request, 'dent/logpatientappointment.html', ctx)

            if Appointment.objects.filter(patient = logpatient.id).count() == 1:
                patientappoint = Appointment.objects.get(patient = logpatient.id)
                ctx = {
                    'appointments':filter_list[2],
                    'appointfilter':filter_list[1],
                    'patientappoint':patientappoint,
                    'formset': formset,
                    'logpatient':logpatient}
                return render(request, 'dent/logpatientappointment.html', ctx)

        ctx = {
            'appointments':filter_list[2],
            'appointfilter':filter_list[1],
            'formset': formset,
            'logpatient':logpatient}
        return render(request, 'dent/logpatientappointment.html', ctx)

    except exceptions.ObjectDoesNotExist:
            return redirect('dent:logpatient', pk = request.user.id)
                

def warningview(request):
    '''Used in both cases, when logged-in patient or not registrated patient try to make an appointment '''
    msg = 'Sorry, but your appointment collides with another appointment and therefore must be deleted'
    ctx= {'msg':msg}
    return render(request, 'dent/warning.html', ctx)
            

#### STAFF ####
@login_required(login_url='dent:login')
@allowed_users(allowed_roles = ['staff'])
def staffprofileview(request,pk): 
    try:
        current_staff = request.user.staff
        update_profile_form = StaffForm(instance = current_staff)
        if request.method == "POST":
            update_profile_form = StaffForm(request.POST, request.FILES, instance = current_staff)
            if update_profile_form.is_valid():
                update_profile_form.save()
                return redirect('dent:staffdetail', pk = request.user.staff.id )
        
        ctx = {'profileform':update_profile_form}
        return render(request, 'dent/staffprofile.html', ctx)

    except:
        profileform = StaffForm()
        if request.method == 'POST':
            profileform = StaffForm(request.POST,request.FILES)
            if profileform.is_valid():
                profileform.save()
                new_doctor_name = profileform.cleaned_data.get('sname')
                new_doctor = Staff.objects.get(sname = new_doctor_name)
                return redirect('dent:staffdetail', pk =  new_doctor.id )

        ctx = {
            'profileform':profileform,
        }
        return render(request, 'dent/staffprofile.html', ctx)


def staffdetailview(request,pk):
    '''
    try points to doctor/nurse detailed view if the profile is filled
    '''
    try: 
        employee = Staff.objects.get(id = pk)
        ctx = {'employee':employee}
        return render(request, 'dent/staffdetail.html',ctx)

    except exceptions.ObjectDoesNotExist:
        try:
            return redirect('dent:staffdetail',pk = request.user.staff.id)

        except:
            return redirect('dent:staffprofile',pk =request.user.id )

#### LIST OF APPOINTMENTS ####
@login_required(login_url='dent:login')
@allowed_users(allowed_roles = ['staff'])
def listview(request):
    ''' 
    List of appointments created only for staff
        -contains patients personal info too
        -can be filtred by patient`s last name, given doctor or appointment date
    '''
    filter_list = filter(request)
    ctx = {
        'appointments':filter_list[2],
        'appointfilter':filter_list[1]}
    return render(request, 'dent/listview.html', ctx)


###### UNLOG PATIENT ######
def unlogpatientview(request):
    ''' View for filling personal info '''
    patientform = PatientForm()
    if request.method == 'POST':
        patientform = PatientForm(request.POST) 
        if patientform.is_valid():
            patientform.save()
            new_patient = Patient.objects.last()
            return redirect('dent:appointment', pk = new_patient.id)

    context = {'patientform':patientform}
    return render(request, 'dent/unlogpatient.html',context)


def appointmentview(request,pk):
    ''' Appointment of patient without registration '''
    unlogpatient = Patient.objects.get(id=pk)
    patientform = PatientForm(instance=unlogpatient)
    appointform = AppointmentForm(initial= {'patient':unlogpatient})
    filter_list = filter(request)
    if request.method == 'POST':
        appointform = AppointmentForm(request.POST)
        print('appointform:',appointform)
        if appointform.is_valid():
            appointform.save()
            return appointmentcheck()

    context = {
            'appointments':filter_list[2],
            'appointfilter':filter_list[1],
            'patientform':patientform,
            'appointform':appointform}
    return render(request, 'dent/unlogappointment.html',context)

#### DETAIL OF EVERY APPOINTMENT ####
def detail(request, pk):
    msg = request.session.get('msg',False)
    if (msg):
        del(request.session['msg'])
    msg = 'Successful registration'
    request.session['msg'] = msg
    appointment = Appointment.objects.get(id=pk)
    # if patient.email:
    #     subject = "Hello from Zubkdent"
    #     message = f"Your registration key is = {patient.id}"
    #     send_mail(
    #         subject,
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         [patient.email],
    #         fail_silently= False,
    #     )
    ctx = {
        'appointment':appointment,
            'message':msg}
    return render(request, 'dent/detail.html', ctx)


#### UPDATE ####
def updateregview(request, pk):
    '''Update of patient without redistration personal info and his/her appointment'''
    update_appointment = Appointment.objects.get(id=pk)
    appointment_patient_id = update_appointment.patient.id
    update_patient = Patient.objects.get(id = appointment_patient_id)
    updateappform = AppointmentForm(instance = update_appointment, initial = {'patient':update_patient, 'time': update_appointment.time} )
    updatepatform = PatientForm(instance = update_patient, initial = {'insurance_c':update_patient.insurance_c}) 
    if request.method == "POST":
        updateappform = AppointmentForm(request.POST, instance=update_appointment)
        updatepatform = PatientForm(request.POST,instance = update_patient)
        if updateappform.is_valid() and updatepatform.is_valid():
            updateappform.save()
            updatepatform.save()
            return redirect('dent:detail', pk = pk)
        
    ctx = {
        'updateappform': updateappform,
        'updatepatform':updatepatform,}
    return render(request, 'dent/updateregview.html', ctx)


#### DELETE ####
class DeleteRegistrationView(View):
    '''
    Delete of patient without redistration personal info and his/her appointment 
    Delete of logged-in patient`s appointment
    '''
    appointments = Appointment.objects.all()
    def get(self,request,pk):
        deleteform = self.appointments.get(id = pk)
        ctx = {'deleteform' : deleteform }
        return render(request, 'dent/deleteregister.html', ctx)
    def post(self, request,pk):
         if request.method == 'POST':
            try:
                if self.appointments.get(id = pk).patient.user.id > 0:
                    self.appointments.get(id = pk).delete()
                    return redirect('dent:home')

            except:
                delete_appointment = Appointment.objects.get(id=pk)
                appointment_patient_id = delete_appointment.patient.id
                Patient.objects.get(id = appointment_patient_id).delete()
                return redirect('dent:home')


#### Patient registration ####
def userpatientregview(request):
    user_patient = CreateUserForm()
    if request.method =='POST':
        user_patient = CreateUserForm(request.POST)
        if user_patient.is_valid():
            user_patient_save = user_patient.save()
            user_patient_name = user_patient.cleaned_data.get('username') 
            patient_group = Group.objects.get(name = 'patients')
            user_patient_save.groups.add(patient_group)
            messages.success(request, 'Account {} was created successful'.format(user_patient_name))
            return redirect('dent:login')

    ctx = {
        'user_patient':user_patient
        }
    return render(request, 'dent/userpatientreg.html',ctx)

#### Staff registration  ####
@login_required(login_url='dent:login')
@allowed_users(allowed_roles = ['staff'])
def staffregview(request):
    ''' Registration is enabled only by superuser'''
    user_form = CreateUserForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user_form_save = user_form.save()
            doctor_nurse = user_form.cleaned_data.get('username')
            staff_group = Group.objects.get(name = 'staff')
            user_form_save.groups.add(staff_group)
            messages.success(
                request, 'Dear {} your account was created successful'
                .format(doctor_nurse))
            return redirect('dent:login')

    context = {
        'user': user_form}
    return render(request, 'dent/staffreg.html', context)


@unauthenticated_user
def loginpage(request):
    '''
        Users are devided into 2 groups, staff and patients groups.
        login differentiate 4 types of user:
            - new staff -> redirect to profile page to throw in personal info
            - staff with filled profile
            - new patient -> redirect to profile page to throw in personal info
            - patient with filled profile
    '''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            if user.groups.filter(name = 'staff').exists():
                try:
                    return redirect('dent:staffdetail', pk = request.user.staff.id)

                except User.staff.RelatedObjectDoesNotExist:
                    return redirect('dent:staffprofile', pk = user.id)

            if user.groups.filter(name = 'patients').exists():
                try:
                    return redirect('dent:logpatientappointment', pk = request.user.patient.id)

                except User.patient.RelatedObjectDoesNotExist:
                    return redirect('dent:logpatient', pk = request.user.id)

        else:
            messages.info(request, 'Incorrect Username or Password')
    return render(request,'dent/login.html')


def logoutpage(request):
    logout(request)
    return redirect('dent:login')


###### SEARCH THE APPOINTMET ######
def searchid(request):
    ''' The appointment is searched accoding it`s id'''
    if request.method == 'POST':
        try:
            searched_id = request.POST['searched_id']
            searched_appointmnet = Appointment.objects.get(id = searched_id)
            return redirect('dent:detail', pk = searched_appointmnet.id)
        except exceptions.ObjectDoesNotExist:
            ctx = {
                'a':'The appointment does not exist with',
                'searched_id': searched_id}
            return render(request, 'dent/search.html', ctx)