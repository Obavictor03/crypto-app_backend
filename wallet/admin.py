from django.contrib import admin
from .models import Wallet
# Register your models here.


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "btc_balance", "get_balance")

    def get_balance(self, obj):
        return obj.balance

    get_balance.short_description = "USD Balance"

    # ❌ Prevent editing USD
    readonly_fields = ("get_balance",)