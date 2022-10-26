import django_filters
from django_filters import DateFilter, CharFilter
from django.forms import widgets
from django import forms
from .models import *


class AppointmentFilter(django_filters.FilterSet):
    date = CharFilter(
        field_name='date', 
        lookup_expr= 'icontains', 
        label = 'Date',
        widget=widgets.DateInput(attrs={
            'type':'date',
            'placeholder': 'MM-DD or MM or DD',
            'id':'datefilter',
            'class':'filteritem',
            'onfocus':"this.value=''"}))
    
    patient = CharFilter(
        field_name = 'patient__sname',
        lookup_expr= 'icontains', 
        label = 'Last name',
        widget=widgets.TextInput(attrs={
            'id':'patientfilter',
            'onfocus':"this.value=''",
            'placeholder':'Filter according to the Last name',
            'class':'filteritem'}))
    
    doctor_char = CharFilter(
        field_name = 'doctor__sname',
        lookup_expr= 'icontains', 
        label = 'Doctor',
        widget=widgets.TextInput(attrs={
            'id':'doctorfilter',
            'class':'filteritem',
            'placeholder':'Filter according to the Doctor',
            'onfocus':"this.value=''"}))
    
    exact_date = DateFilter(
        field_name = 'date',
        lookup_expr= 'exact',
        label = 'Date',
        widget=widgets.TextInput(attrs={
            'type':'date',
            'id':'exact-date',
            'class':'text-input',
            'onfocus':"this.value=''"}))

    # doctor = CharFilter(
    #     field_name = 'doctor',
    #     lookup_expr= 'exact',
    #     label = 'Doctor',
    #     widget=widgets.Select(attrs={
    #         'class':'text-input'}))

    # doctor = forms.CharField(widget=forms.Select(attrs = {'class':'text-input'}))
    
    class Meta:
        model= Appointment
        fields = []
        fields = '__all__'
        # widgets ={'doctor':forms.Select(attrs = {'class':'text-input'})}


#### APPOINTMENTS FILTERING ####
def filter(request,appointments):
    appointments = appointments
    appointfilter = AppointmentFilter(request.GET, queryset=appointments)
    appointments = appointfilter.qs
    filter_list = [appointments, appointfilter, appointments]
    return filter_list