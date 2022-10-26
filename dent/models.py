from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
import string
import random


class Staff(models.Model):
    TITLES = (
        ('Dr', 'Dr'),
        ('MDDr', 'MDDr'),
        ('MUDr', 'MUDr'),
        ('Bc','Bc'),
        ('Mrs', 'Mrs'),
        ('Mr', 'Mr'),
    )
    FIELDS = (
        ('Dental Surgery', 'Dental Surgery'),
        ('Stomatology', 'Stomatology'),
        ('Implantology', 'Implantology'),
        ('Dental Hygiene', 'Dental Hygiene'),
        ('Administrator','Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, choices = TITLES)
    fname = models.CharField(max_length = 100)
    sname = models.CharField(max_length= 100)
    about = models.TextField(null= True, blank = True)
    profile_pic = models.ImageField(null = True, blank= True)
    field = models.CharField(max_length=250, choices = FIELDS, default=000)
    
    def __str__(self):
        return self.sname


class Meta:
    db_table = 'Patient`s data'

class Patient(models.Model):
    COMPANIES = (
        ('GHI', 'GHI'),
        ('Confidence', 'Confidence'),
        ('Union', 'Union'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True, blank = True)
    fname = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)
    insurance_c = models.CharField(max_length=20,choices=COMPANIES)
    cell_phone_num = models.IntegerField()
    email = models.EmailField(max_length= 254, null = True, blank= True) 
    def __str__(self):
        return self.fname
        

class Appointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete= models.CASCADE)
    doctor = models.ForeignKey('Staff', on_delete = models.CASCADE)
    key = models.CharField(max_length = 15, null = True)
    date = models.DateField(auto_now_add= False)
    time = models.TimeField(auto_now_add=False)
    notes = models.TextField(null=True, blank = True)



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


def keygen(length = 10, code = string.ascii_uppercase + string.digits):
    key = ''.join(random.choice(code) for _ in range(length))
    return key


def sendemail(request, appointment):
    if request.method =="POST":
        if appointment.patient.email:
            subject = "Hello from 987dent"
            message = f"Your registration key is = {appointment.key}"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [appointment.patient.email],
                fail_silently= False,
            )
            msg = f'The email with appointment details was sent to: {appointment.patient.email}'
            return msg

    









