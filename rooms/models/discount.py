from django.db import models


class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage'),
    ]

    discount_id = models.IntegerField(unique=True)
    discount_name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.discount_name
