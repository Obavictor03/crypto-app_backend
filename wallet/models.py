from django.db import models
from django.conf import settings
from .utils import get_btc_price

# Create your models here.
User = settings.AUTH_USER_MODEL

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    btc_balance = models.FloatField(default=0)  # Starting BTC balance for testing

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    @property
    def balance(self):
        btc_price = get_btc_price()
        return self.btc_balance * btc_price

   def add_btc(self, amount):
        self.btc_balance += amount
        self.save()