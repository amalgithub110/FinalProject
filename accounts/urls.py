from django .urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.Loginview, name='login'),
    path('logout/',views.Logoutview,name='logout'),
    path('identifyuser/',views.identifyuserview,name='identifyuser'),
    path('OTPView/<str:en_uname>/', views.OTPView, name='otp'),
    path('resetpassword/<en_uname>/', views.resetpassword, name='resetpassword'),

]