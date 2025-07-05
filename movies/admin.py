from django.contrib import admin
from .models import Movie,Cast
# Register your models here.

@admin.register(Movie)
class UserAdmin(admin.ModelAdmin):
    list_display=('title','language','status')


@admin.register(Cast)
class UserAdmin(admin.ModelAdmin):
    list_display=('movie','name','role','image')