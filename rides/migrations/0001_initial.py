# Generated by Django 4.1.1 on 2022-11-11 23:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('recurrent_rides', '0001_initial'),
        ('cities', '0001_initial'),
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.CharField(choices=[('accepted', 'Accepted'), ('declined', 'Declined'), ('pending', 'Pending'), ('cancelled', 'Cancelled')], default='pending', max_length=9)),
                ('reserved_seats', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('ride_id', models.AutoField(primary_key=True, serialize=False)),
                ('area_from', models.CharField(blank=True, default='', max_length=100)),
                ('area_to', models.CharField(blank=True, default='', max_length=100)),
                ('start_date', models.DateTimeField()),
                ('duration', models.DurationField(default=datetime.timedelta)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('seats', models.PositiveIntegerField()),
                ('recurrent', models.BooleanField(default=False)),
                ('automatic_confirm', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, default='')),
                ('available_seats', models.IntegerField(blank=True, null=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('city_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city_from', to='cities.city')),
                ('city_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city_to', to='cities.city')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver', to='users.user')),
                ('passengers', models.ManyToManyField(blank=True, through='rides.Participation', to='users.user')),
                ('recurrent_ride', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='single_rides', to='recurrent_rides.recurrentride')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ride', to='vehicles.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='participation',
            name='ride',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rides.ride'),
        ),
        migrations.AddField(
            model_name='participation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passenger', to='users.user'),
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('coordinate_id', models.AutoField(primary_key=True, serialize=False)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=15)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=15)),
                ('sequence_no', models.IntegerField()),
                ('ride', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coordinates', to='rides.ride')),
            ],
        ),
    ]
