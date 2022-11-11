import datetime


def get_city_info(parameters: dict, which_city: str) -> dict:
    """
    Converts parameters to more readable dictionary with city info.

    :param parameters: parameters from user
    :param which_city: from or to
    :return: dictionary with city data
    """
    return {"name": parameters[f'city_{which_city}'], "state": parameters[f'city_{which_city}_state'],
            "county": parameters[f'city_{which_city}_county'], "lat": parameters[f'city_{which_city}_lat'],
            "lng": parameters[f'city_{which_city}_lng']}


def filter_rides_by_cities(request, queryset):
    try:
        city_from_dict = get_city_info(request.GET, 'from')
        queryset = queryset.filter(city_from__name=city_from_dict['name'], city_from__state=city_from_dict['state'],
                                   city_from__county=city_from_dict['county'])
    except KeyError:
        pass

    try:
        city_to_dict = get_city_info(request.GET, 'to')
        queryset = queryset.filter(city_to__name=city_to_dict['name'], city_to__state=city_to_dict['state'],
                                   city_to__county=city_to_dict['county'])
    except KeyError:
        pass

    return queryset


def daterange_filter(queryset, name: str, value: datetime):
    first_parameter = '__'.join([name, 'gte'])
    second_parameter = '__'.join([name, 'lte'])
    return queryset.filter(**{first_parameter: value,
                              second_parameter: datetime.datetime.combine(value.date() + datetime.timedelta(1),
                                                                          datetime.time.max)})
