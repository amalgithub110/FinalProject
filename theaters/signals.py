# theaters/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Theater, Seat

@receiver(post_save, sender=Theater)
def create_seats_for_theater(sender, instance, created, **kwargs):
    if created:
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']  # 10 rows
        seats_per_row = 10  # 10 seats per row

        for row in rows:
            if row in ['A', 'B', 'C']:
                seat_type = 'platinum'
            elif row in ['D', 'E', 'F', 'G']:
                seat_type = 'gold'
            else:
                seat_type = 'silver'

            for seat_number in range(1, seats_per_row + 1):
                Seat.objects.create(
                    theater=instance,
                    row_label=row,
                    seat_number=seat_number,
                    seat_type=seat_type
                )
