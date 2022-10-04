from django.contrib import admin
from .models import Appointment, Patient, Staff

# Register your models here.

admin.site.register(Patient)
admin.site.register(Staff)
admin.site.register(Appointment)
