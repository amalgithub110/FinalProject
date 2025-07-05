from django.urls import path
from . import views
urlpatterns = [
    path('review/<slug>/',views.add_review_view,name='review'),
]