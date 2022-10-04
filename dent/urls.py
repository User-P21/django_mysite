from django.urls import path
from . import views

app_name = 'dent'
urlpatterns = [
    path('',views.home, name = 'home'),
    path('searchid/',views.searchid, name = 'searchid'),
    path('userpatientreg/', views.userpatientregview, name = 'userpatientreg'),
    path('staffreg/',views.staffregview, name = 'staffreg'),
    path('login/', views.loginpage, name= 'login'),
    path('logout/', views.logoutpage, name= 'logout'),
    path('list/', views.listview, name = 'listo'),
    path('logpatient/<int:pk>', views.logpatientview, name = 'logpatient'),
    path('logpatientappointment/<int:pk>', views.logpatientappointmentview, name = 'logpatientappointment'),
    path('warning',views.warningview, name = 'warning'),
    path('staffprofile/<int:pk>',views.staffprofileview, name = 'staffprofile'),
    path('<int:pk>/',views.detail, name = 'detail'),
    path('staffdetail/<int:pk>',views.staffdetailview, name = 'staffdetail'),
    path('unlogpatient/', views.unlogpatientview, name= 'unlogpatient'),
    path('appointment/<int:pk>', views.appointmentview, name= 'appointment'),
    path('updateregview/<int:pk>', views.updateregview, name= 'updateregview'),
    path('registration/<int:pk>/delete', views.DeleteRegistrationView.as_view(), name = 'deleteregistration'),
    ]