from rest_framework import serializers

from cities.serializers import CitySerializer
from recurrent_rides.models import RecurrentRide
from rides.models import Ride
from rides.serializers import get_duration
from users.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer


class RecurrentRideSerializer(serializers.ModelSerializer):
    city_from = CitySerializer(many=False)
    city_to = CitySerializer(many=False)
    driver = UserSerializer(many=False, required=False)
    vehicle = VehicleSerializer(many=False, required=False)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = RecurrentRide
        fields = (
            'ride_id', 'city_from', 'city_to', 'area_from', 'area_to', 'start_date', 'end_date', 'frequency_type',
            'frequence', 'occurrences', 'price', 'seats', 'automatic_confirm', 'description', 'driver', 'vehicle',
            'duration')
        depth = 1

    def get_duration(self, obj):
        return get_duration(obj)


class RecurrentRidePersonal(serializers.ModelSerializer):
    city_from = CitySerializer(many=False)
    city_to = CitySerializer(many=False)
    duration = serializers.SerializerMethodField()
    driver = UserSerializer(many=False)

    class Meta:
        model = Ride
        fields = (
            'ride_id', 'city_from', 'city_to', 'area_from', 'area_to', 'start_date', 'duration', 'driver')
        extra_kwargs = {'area_from': {'required': False}, 'area_to': {'required': False}}

    def get_duration(self, obj):
        return get_duration(obj)


class SingleRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('ride_id', 'start_date')
