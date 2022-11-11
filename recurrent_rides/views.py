from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter

from django_filters import rest_framework as filters

from recurrent_rides.filters import RecurrentRideFilter
from recurrent_rides.models import RecurrentRide
from recurrent_rides.serializers import RecurrentRideSerializer, RecurrentRidePersonal, SingleRideSerializer
from utils.CustomPagination import CustomPagination
from utils.generic_endpoints import get_paginated_queryset
from utils.utils import filter_rides_by_cities
from utils.validate_token import validate_token


# Create your views here.
class RecurrentRideViewSet(viewsets.ModelViewSet):
    serializer_classes = {
        'user_rides': RecurrentRidePersonal,
        'retrieve': RecurrentRideSerializer,
        'single_rides': SingleRideSerializer,
    }
    queryset = RecurrentRide.objects.filter()
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = RecurrentRideFilter
    pagination_class = CustomPagination
    ordering_fields = ['price', 'start_date', 'duration']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action) or RecurrentRideSerializer

    def _get_user_rides(self, request, user):
        queryset = self.get_queryset()
        rides = queryset.filter(driver=user)

        rides = filter_rides_by_cities(request, rides)
        filtered_rides = self.filter_queryset(rides)
        return get_paginated_queryset(self, filtered_rides)

    @validate_token
    @action(detail=False, methods=['get'])
    def user_rides(self, request, *args, **kwargs):
        """
        Endpoint for getting user recurrent rides. Can be filtered with price (from - to), from place, to place
        :param request:
        :return: List of user's recurrent rides.
        """
        user = kwargs['user']

        return self._get_user_rides(request, user)

    def _get_singular_rides(self, request, user):
        instance = self.get_object()
        if instance.driver == user:
            params = {}
            start_date = request.GET.get('single_start_date', None)
            if start_date:
                params['start_date__gt'] = start_date

            rides = instance.single_rides.filter(**params)[:10]
            serializer = self.get_serializer(rides, many=True)
            return JsonResponse(status=status.HTTP_200_OK, data=serializer.data, safe=False)
        else:
            return JsonResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED, data="User not allowed to get rides",
                                safe=False)

    @validate_token
    @action(detail=True, methods=['get'])
    def single_rides(self, request, *args, **kwargs):
        user = kwargs['user']
        return self._get_singular_rides(request, user)
