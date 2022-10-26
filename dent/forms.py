from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Staff, Appointment
from betterforms.multiform import MultiModelForm


import datetime as dt


HOUR_CHOICES = (
    ("08:00","08:00"),
    ("09:00","09:00"),
    ("10:00","10:00"),
    ("11:00","11:00"),
    ("13:00","13:00"),
    ("14:00","14:00"),
)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2', 'is_staff']
        widgets = {
            'is_staff': forms.CheckboxInput(attrs={'checked' : ''})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = {'class':'text-input'}
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(data)


class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'user': forms.TextInput(attrs={'readonly':'',}),
            'profile_pic': forms.FileInput()
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        data = {'class':'text-input'}
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(data)
            self.fields['about'].widget.attrs.update({'class':'textarea-input'})


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'user':forms.TextInput(attrs={'type':'hidden'}),
            'fname':forms.TextInput(attrs={
                'type':'text',
                'id':'fname',}),
            'sname':forms.TextInput(attrs={
                'type':'text',
                'id':'sname'}),
            'insurance_c':forms.Select(attrs={
                'id':'insurance_c'}),
            'cell_phone_num':forms.NumberInput(attrs={
                'id':'cell_phone_num'}),
            'email':forms.EmailInput(attrs={
                'id':'email',
                'placeholder':'We send there the Registration Key '}),
         }
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        data = {'class':'text-input'}
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(data)


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'key':forms.TextInput(attrs = {'class':'text-input', 'readonly':'', 'type':'hidden'}),
            'doctor':forms.Select(attrs = {'class':'text-input'}),
            'date':forms.DateInput(attrs={'type':'date','class':'text-input'}),
            'time':forms.Select(choices=HOUR_CHOICES,attrs={'class':'text-input'}),
            'notes':forms.Textarea(attrs={'class':'textarea-input'}),
         }




    