from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.FloatField()  # Starting balance for testing
    btc_balance = models.FloatField(default=6.30000000)  # Starting BTC balance for testing

    def __str__(self):
        return f"{self.user.username}'s Wallet"