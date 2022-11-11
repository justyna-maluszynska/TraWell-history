from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models

from cities.models import City
from users.models import User
from vehicles.models import Vehicle


class RecurrentRide(models.Model):
    class FrequencyType(models.TextChoices):
        HOURLY = 'hourly'
        DAILY = 'daily'
        WEEKLY = 'weekly'
        MONTHLY = 'monthly'

    class WeekDays(models.TextChoices):
        MONDAY = 'MON'
        TUESDAY = 'TUE'
        WEDNESDAY = 'WED'
        THURSDAY = 'THU'
        FRIDAY = 'FRI'
        SATURDAY = 'SAT'
        SUNDAY = 'SUN'

    ride_id = models.AutoField(primary_key=True)
    city_from = models.ForeignKey(City, related_name='recur_city_from', blank=False, null=True,
                                  on_delete=models.SET_NULL)
    city_to = models.ForeignKey(City, related_name='recur_city_to', blank=False, null=True, on_delete=models.SET_NULL)
    area_from = models.CharField(max_length=100, blank=True, default="")
    area_to = models.CharField(max_length=100, blank=True, default="")
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    frequency_type = models.CharField(choices=FrequencyType.choices, default=FrequencyType.DAILY, max_length=9)
    frequence = models.IntegerField(default=1, blank=False, null=False)
    occurrences = ArrayField(models.CharField(max_length=10, choices=WeekDays.choices), blank=True, null=True)
    duration = models.DurationField(blank=False, default=timedelta)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    seats = models.PositiveIntegerField(null=False)
    automatic_confirm = models.BooleanField(null=False, default=False)
    description = models.TextField(blank=True, default="")
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, blank=False, null=True)
    is_cancelled = models.BooleanField(default=False, blank=False)
