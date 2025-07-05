from django.shortcuts import render,redirect
from .models import Review
from movies.models import Movie
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def add_review_view(request, slug):
    user =User.objects.get(username=request.user.username)
    if not Movie.objects.filter(slug=slug).exists():
        messages.error(request, "Movie does not exist.")
        return redirect('recommended_movies') 
    movie = Movie.objects.get(slug=slug)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        Review.objects.create(
            user=user,
            movie=movie,
            rating=rating,
            review_text=review_text
        )
        messages.success(request, "Review added successfully.")
        return redirect('movie_detail', slug=slug)
    return render(request, 'reviews/add_review.html')

    

       