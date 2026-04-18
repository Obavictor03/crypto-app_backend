from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from wallet.models import Wallet
import requests


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        # 🔥 Fetch live BTC price
        try:
            res = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            )
            data = res.json()
            btc_price = data["bitcoin"]["usd"]
        except:
            btc_price = 0  # fallback

        default_btc = 6.3
        usd_value = default_btc * btc_price

        Wallet.objects.create(
            user=instance,
            btc_balance=default_btc,
            balance=usd_value
        )