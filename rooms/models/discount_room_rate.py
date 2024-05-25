from django.db import models

from rooms.models.discount import Discount
from rooms.models.room_rate import RoomRate


class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room_rate.room_name} - {self.discount.discount_name}"
