from django.shortcuts import render, get_object_or_404
from .models import Movie , Cast
from reviews.models import Review  # Make sure you import the Review model
from django.db.models import Avg
from django.contrib.auth.models import User  # or use get_user_model()
import datetime

# Create your views here.


def some_view(request):
    if request.user.is_authenticated:
        print(request.user.username)


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, slug):
    movie = Movie.objects.get(slug=slug)
    reviews = Review.objects.filter(movie=movie)
    rating = reviews.aggregate(avg=Avg('rating'))['avg']
    if rating is None:
        rating = 0
    if (rating - int(rating)) > 0:
        rating = '{:.1f}'.format(rating)
    else:
        rating = int(rating)
    context = {
        'movie': movie,
        'rating': rating,
        'reviews': reviews,
        'date' : datetime.date.today()

    }

    return render(request, 'movies/movie_detail.html', context)


