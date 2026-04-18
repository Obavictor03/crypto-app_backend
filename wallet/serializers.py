from rest_framework import serializers
from .models import Wallet
from .utils import get_btc_price

class WalletSerializer(serializers.ModelSerializer):
    usd_balance = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ['btc_balance', 'usd_balance']

    def get_usd_balance(self, obj):
        price = get_btc_price()
        return obj.btc_balance * price