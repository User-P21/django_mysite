from django.db import models
from django.contrib.auth.models import User


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
    date = models.DateField(auto_now_add= False)
    time = models.TimeField(auto_now_add=False)
    notes = models.TextField(null=True, blank = True)










