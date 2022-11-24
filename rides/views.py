from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action

from rides.filters import RideFilter
from rides.models import Ride, Participation
from rides.serializers import RideSerializer, RideListSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from utils.generic_endpoints import get_paginated_queryset
from utils.utils import filter_rides_by_cities
from utils.CustomPagination import CustomPagination
from utils.validate_token import validate_token

from history_microservice import tasks


class RideViewSet(viewsets.ModelViewSet):
    """
    API View Set that allows Rides to be viewed, created, updated or deleted.
    This View Set automatically provides list and detail actions.
    """

    serializer_classes = {
        'retrieve': RideSerializer,
        'user_rides': RideListSerializer,
    }
    queryset = Ride.objects.filter()
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = RideFilter
    pagination_class = CustomPagination
    ordering_fields = ['price', 'start_date', 'duration', 'available_seats']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action) or RideSerializer

    def _get_user_rides(self, request, user):
        try:
            user_ride_type = request.GET['user_type']
            queryset = self.get_queryset()

            if user_ride_type == 'driver':
                rides = queryset.filter(driver=user)
            elif user_ride_type == 'passenger':
                rides = queryset.filter(passengers=user, participation__decision=Participation.Decision.ACCEPTED)
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Invalid user_type parameter", safe=False)
        except KeyError as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=f"Missing parameter {e}", safe=False)

        rides = filter_rides_by_cities(request, rides)
        filtered_rides = self.filter_queryset(rides)
        return get_paginated_queryset(self, filtered_rides)

    @validate_token
    @action(detail=False, methods=['get'])
    def user_rides(self, request, *args, **kwargs):
        """
        Endpoint for getting user rides. Can be filtered with price (from - to), from place, to place
        :param request:
        :return: List of user's rides.
        """
        user = kwargs['user']

        return self._get_user_rides(request, user)
