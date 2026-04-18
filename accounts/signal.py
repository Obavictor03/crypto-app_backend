from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from wallet.models import Wallet
import requests


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        default_btc = 6.3

        btc_price = 67000  # ✅ default fallback FIRST

        # 🔥 Try fetching live price
        try:
            res = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
                timeout=5
            )
            data = res.json()

            # ✅ Safe extraction
            btc_price = data.get("bitcoin", {}).get("usd", btc_price)

        except Exception as e:
            print("BTC price fetch failed:", e)

        usd_value = default_btc * btc_price

        Wallet.objects.create(
            user=instance,
            btc_balance=default_btc,
            balance=usd_value
        )