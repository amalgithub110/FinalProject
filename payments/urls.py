from django.urls import path
from . import views

urlpatterns=[
    path('payment/<int:booking_id>/',views.payment_view,name='payment'),
    path('success/<int:booking_id>/',views.success_view,name='success'),
    path('cancel/<int:booking_id>/',views.cancel_view,name='cancel')
]