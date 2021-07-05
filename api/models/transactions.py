from django.db import models

from api.models import Reservation


class Transaction(models.Model):
    EURO = 'EU'
    OTHER = 'other'

    CURRENCIES = (
        (EURO, "Euro"),
        (OTHER, 'other')
    )

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.IntegerField()
    currency = models.CharField(choices=CURRENCIES, null=True, blank=True, max_length=250)