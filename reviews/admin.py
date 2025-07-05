from django.contrib import admin
from .models import Review

# Register your models here.

@admin.register(Review)
class UserAdmin(admin.ModelAdmin):
    list_display=('rating','review_text')

