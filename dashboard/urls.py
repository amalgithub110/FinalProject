from django.urls import path
from . import views
urlpatterns = [
    path('order/',views.YourOrder,name='order'),
    path('search/', views.SearchView, name='search')
]