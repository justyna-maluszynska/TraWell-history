from rest_framework import serializers

from cities.serializers import CitySerializer
from rides.models import Ride, Participation, Coordinate
from users.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer


class ParticipationListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(decision='accepted')
        return super(ParticipationListSerializer, self).to_representation(data)


class ParticipationNestedSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Participation
        fields = ('id', 'user', 'decision')
        list_serializer_class = ParticipationListSerializer


class CoordinatesNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ('lat', 'lng', 'sequence_no')


class RideListSerializer(serializers.ModelSerializer):
    city_from = CitySerializer(many=False)
    city_to = CitySerializer(many=False)
    driver = UserSerializer(many=False)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = (
            'ride_id', 'city_from', 'city_to', 'area_from', 'area_to', 'start_date', 'price', 'seats', 'driver',
            'duration', 'available_seats')
        extra_kwargs = {'area_from': {'required': False}, 'area_to': {'required': False}}

    def get_duration(self, obj):
        return get_duration(obj)


class RideSerializer(serializers.ModelSerializer):
    city_from = CitySerializer(many=False)
    city_to = CitySerializer(many=False)
    driver = UserSerializer(many=False, required=False)
    vehicle = VehicleSerializer(many=False, required=False)
    duration = serializers.SerializerMethodField()
    passengers = ParticipationNestedSerializer(source='participation_set', many=True, required=False)
    coordinates = CoordinatesNestedSerializer(many=True)

    class Meta:
        model = Ride
        fields = ('ride_id', 'city_from', 'city_to', 'area_from', 'area_to', 'start_date', 'price', 'seats',
                  'recurrent', 'automatic_confirm', 'description', 'driver', 'vehicle', 'duration', 'available_seats',
                  'passengers', 'coordinates')
        depth = 1

    def get_duration(self, obj):
        return get_duration(obj)


def get_duration(obj: Ride):
    total_minutes = int(obj.duration.total_seconds() // 60)
    hours = total_minutes // 60
    return {'hours': hours, 'minutes': total_minutes - hours * 60}
