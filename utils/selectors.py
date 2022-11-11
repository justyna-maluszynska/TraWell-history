from cities.models import City
from users.models import User
from vehicles.models import Vehicle


def city_object(city: dict) -> City | None:
    """
    Finds requested city in database and returns its object.

    :param city: dictionary with city data
    :return: found City object or None
    """
    try:
        city_obj = City.objects.get(name=city['name'], state=city['state'], county=city['county'])
        return city_obj
    except City.DoesNotExist:
        return None


def user_vehicle(data: dict, user: User) -> Vehicle or None:
    """
    Finds vehicle with given id, that belongs to given user.

    :param data: dictionary containing vehicle id
    :param user: owner of vehicle
    :return: found Vehicle object or None
    """
    try:
        vehicle = None
        vehicle_id = data.pop('vehicle')
        if user.private:
            vehicle = Vehicle.objects.get(vehicle_id=vehicle_id, user=user)
        return vehicle
    except (KeyError, Vehicle.DoesNotExist):
        return None
