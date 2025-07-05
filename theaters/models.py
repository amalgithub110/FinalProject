from django.db import models
from movies.models import Movie

# Create your models here.
class Theater(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f'{self.name}-{self.city}'
    
seat_type =[
    ('silver','silver'),
    ('gold','gold'),
    ('platinum','platinum')
]    
class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    row_label = models.CharField(max_length=1)
    seat_number = models.IntegerField()
    seat_type = models.CharField(max_length=100,choices=seat_type)

    def __str__(self):
        return f"{self.row_label}{self.seat_number}"


class showtime(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showtime = models.DateTimeField()
    silver_seats_price = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    gold_seats_price = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    platinum_seats_price = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    