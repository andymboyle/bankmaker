from django.db import models
from django.conf import settings


class Card(models.Model):
    name = models.CharField(max_length=50, blank=True)
    card_number = models.IntegerField(max_length=19)
    luhn_check = models.BooleanField()
    limit = models.IntegerField()
    balance = models.IntegerField(default=0)
