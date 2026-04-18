from django.contrib import admin
from .models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "btc_balance", "get_balance")
    readonly_fields = ("get_balance",)

    def get_balance(self, obj):
        return obj.balance

    get_balance.short_description = "USD Balance"

    # ❌ Disable adding new wallets manually
    def has_add_permission(self, request):
        return False