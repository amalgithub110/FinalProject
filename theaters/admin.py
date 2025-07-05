from django.contrib import admin
from . models import Theater,Seat,showtime

# Register your models here.
@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city','address')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('theater','row_label','seat_number','seat_type')

@admin.register(showtime)
class showtimeAdmin(admin.ModelAdmin):
    list_display = ('theater','movie','showtime','silver_seats_price','gold_seats_price','platinum_seats_price')
    
    
