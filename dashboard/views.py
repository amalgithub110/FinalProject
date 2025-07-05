from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from movies.models import Movie
from accounts.models import User
from bookings.models import Booking
from theaters.models import showtime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def home(request):
    movies=Movie.objects.all()
    context={
        'movies': movies
    }
    return render(request,'dashboard/home.html',context)


def SearchView(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        movies = Movie.objects.filter(title__icontains=search_query)  # <-- use icontains for partial, case-insensitive match
        context = {'movies': movies}
        return render(request, 'dashboard/home.html', context)
    return redirect('movies')



@login_required
def YourOrder(request):
    user= request.user
    bookings_qs=Booking.objects.filter(user=user)
    context= {'bookings':bookings_qs}
    return render(request,'dashboard/b_t.html',context)

