# utils.py or inside your view
import requests
from django.core.cache import cache

def get_btc_price():
    cached_price = cache.get("btc_price")

    if cached_price:
        return cached_price

    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    res = requests.get(url).json()

    try:
        price = res["bitcoin"]["usd"]
    except:
        price = 0

    cache.set("btc_price", price, timeout=60)  # cache for 1 min
    return price