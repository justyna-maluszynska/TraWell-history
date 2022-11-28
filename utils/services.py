import datetime

from rides.models import Participation, Ride, Coordinate
from users.models import User
from cities.models import City
from vehicles.models import Vehicle
from recurrent_rides.models import RecurrentRide


def archive_rides(rides):
    for ride in rides:
        city_from = ride.pop('city_from')
        city_to = ride.pop('city_to')
        driver = ride.pop('driver')
        vehicle = None
        try:
            vehicle = ride.pop('vehicle')
        except KeyError:
            pass
        city_from_obj = get_or_create_city(city_from)
        city_to_obj = get_or_create_city(city_to)
        driver_obj = get_or_create_user(driver)
        vehicle_obj = None
        if vehicle:
            vehicle_obj = get_or_create_vehicle(vehicle)

        duration = get_duration(ride.pop('duration'))

        passengers = ride.pop('passengers')

        recurrent_ride = ride.pop('recurrent_ride')
        if recurrent_ride:
            recurrent_ride.update(
                {'driver': driver_obj, 'city_from': city_from_obj, 'city_to': city_to_obj, 'duration': duration})

            recurrent_ride_obj, created = RecurrentRide.objects.update_or_create(ride_id=recurrent_ride['ride_id'],
                                                                                 defaults=recurrent_ride)
        else:
            recurrent_ride_obj = None
        ride.update({'driver': driver_obj, 'city_from': city_from_obj, 'city_to': city_to_obj, 'duration': duration,
                     'recurrent_ride': recurrent_ride_obj})
        if vehicle_obj:
            ride.update({'vehicle': vehicle_obj})
        ride_obj, created = Ride.objects.update_or_create(ride_id=ride['ride_id'], defaults=ride)

        for passenger in passengers:
            passenger_obj = get_or_create_user(passenger)
            get_or_create_participation(passenger=passenger_obj, ride=ride_obj)


def get_or_create_city(city):
    city_id = city['city_id']
    city_obj, created = City.objects.update_or_create(city_id=city_id, defaults=city)
    return city_obj


def get_or_create_user(user):
    user_id = user['user_id']
    user_obj, created = User.objects.update_or_create(user_id=user_id, defaults=user)
    return user_obj


def get_or_create_vehicle(vehicle):
    vehicle_id = vehicle['vehicle_id']

    driver = get_or_create_user(vehicle['user'])
    vehicle_obj, created = Vehicle.objects.update_or_create(vehicle_id=vehicle_id, user=driver, defaults=vehicle)
    return vehicle_obj


def get_duration(duration):
    t = datetime.datetime.strptime(duration, "%H:%M:%S")
    td2 = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return td2


def get_or_create_participation(passenger, ride):
    participation, created = Participation.objects.update_or_create(ride_id=ride.ride_id, user_id=passenger.user_id,
                                                                    defaults={'decision': 'accepted'})
    return participation
