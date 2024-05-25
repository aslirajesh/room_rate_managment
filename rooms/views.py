import pandas as pd
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate
from .serializers import RoomRateSerializer, OverriddenRoomRateSerializer, DiscountSerializer, DiscountRoomRateSerializer
from django.shortcuts import get_object_or_404


class RoomRateViewSet(viewsets.ModelViewSet):
    queryset = RoomRate.objects.all()
    serializer_class = RoomRateSerializer


class OverriddenRoomRateViewSet(viewsets.ModelViewSet):
    queryset = OverriddenRoomRate.objects.all()
    serializer_class = OverriddenRoomRateSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class DiscountRoomRateViewSet(viewsets.ModelViewSet):
    queryset = DiscountRoomRate.objects.all()
    serializer_class = DiscountRoomRateSerializer


class RateViewSet(viewsets.ViewSet):
    # add swagger schema
    @swagger_auto_schema(
        operation_summary='Get lowest rate for a room on a specific date',
        manual_parameters=[
            openapi.Parameter(
                name='room_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description='Room ID',
            ),
            openapi.Parameter(
                name='date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description='Date',
            ),
        ],
    )
    @action(detail=False, methods=['get'])
    def lowest_rate(self, request):
        room_id = request.GET.get('room_id')
        date = request.GET.get('date')
        room_rate = get_object_or_404(RoomRate, room_id=room_id)
        final_rate = self.get_lowest_rate(room_rate, date)
        return Response(
            {'room_id': room_id, 'date': date, 'lowest_rate': final_rate},
            status=200
        )

    @swagger_auto_schema(
        operation_summary='Get lowest rate for a room within a date range',
        manual_parameters=[
            openapi.Parameter(
                name='room_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description='Room ID',
            ),
            openapi.Parameter(
                name='start_date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description='Start date',
            ),
            openapi.Parameter(
                name='end_date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description='End date',
            ),
        ],
    )
    @action(detail=False, methods=['get'])
    def filter_rates(self, request):
        room_id = request.GET.get('room_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        room_rate = get_object_or_404(RoomRate, room_id=room_id)
        date_range = pd.date_range(start=start_date, end=end_date)
        rates = []

        for date in date_range:
            lowest_rate = self.get_lowest_rate(room_rate, date)
            rates.append({
                'date': date,
                'lowest_rate': lowest_rate,
            })

        return Response({
            'room_id': room_id,
            'room_name': room_rate.room_name,
            'rates': rates
        })

    def get_lowest_rate(self, room_rate, stay_date):
        try:
            overridden_rate = OverriddenRoomRate.objects.get(room_rate=room_rate, stay_date=stay_date).overridden_rate
        except OverriddenRoomRate.DoesNotExist:
            overridden_rate = room_rate.default_rate

        discounts = DiscountRoomRate.objects.filter(room_rate=room_rate)
        max_discount_value = 0
        for discount_room_rate in discounts:
            discount = discount_room_rate.discount
            if discount.discount_type == 'fixed':
                discount_value = discount.discount_value
            elif discount.discount_type == 'percentage':
                discount_value = overridden_rate * discount.discount_value / 100
            if discount_value > max_discount_value:
                max_discount_value = discount_value

        final_rate = overridden_rate - max_discount_value
        return final_rate
