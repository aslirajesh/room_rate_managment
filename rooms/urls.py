from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomRateViewSet, OverriddenRoomRateViewSet, DiscountViewSet, DiscountRoomRateViewSet, RateViewSet

router = DefaultRouter()
router.register('room_rates', RoomRateViewSet)
router.register('overridden_room_rates', OverriddenRoomRateViewSet)
router.register('discounts', DiscountViewSet)
router.register('discount_room_rates', DiscountRoomRateViewSet)
router.register('rates', RateViewSet, basename='rates')

urlpatterns = [
    path('', include(router.urls)),
]
