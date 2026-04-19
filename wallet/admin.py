from django.contrib import admin
from .models import Wallet

# ✅ Admin Action
@admin.action(description="Add BTC to selected wallets")
def add_btc(modeladmin, request, queryset):
    for wallet in queryset:
        wallet.add_btc(6.07)  # 🔥 Simple fixed amount


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "btc_balance", "get_balance")
    readonly_fields = ("get_balance",)
    actions = [add_btc]

    def get_balance(self, obj):
        return obj.balance

    get_balance.short_description = "USD Balance"

    def has_add_permission(self, request):
        return False