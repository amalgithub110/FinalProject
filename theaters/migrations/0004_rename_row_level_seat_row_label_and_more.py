# Generated by Django 5.2.2 on 2025-07-04 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theaters', '0003_showtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seat',
            old_name='row_level',
            new_name='row_label',
        ),
        migrations.RenameField(
            model_name='seat',
            old_name='seat_no',
            new_name='seat_number',
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='dimond_price',
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='gold_price',
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='silver_price',
        ),
        migrations.AddField(
            model_name='showtime',
            name='gold_seats_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='showtime',
            name='platinum_seats_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='showtime',
            name='silver_seats_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='seat',
            name='seat_type',
            field=models.CharField(choices=[('silver', 'silver'), ('gold', 'gold'), ('platinum', 'platinum')], max_length=100),
        ),
        migrations.AlterField(
            model_name='theater',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='theater',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
