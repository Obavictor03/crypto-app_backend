from django.contrib import admin
from .models import Wallet
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME


# ✅ FORM
class AddBTCForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    amount = forms.FloatField(label="BTC Amount", min_value=0.00000001)


# ✅ ADMIN ACTION
@admin.action(description="Add BTC (custom amount)")
def add_btc(modeladmin, request, queryset):

    # 🔥 When admin clicks APPLY
    if request.POST.get("apply"):
        form = AddBTCForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            # ✅ VERY IMPORTANT: get selected IDs properly
            selected = request.POST.getlist(ACTION_CHECKBOX_NAME)

            wallets = Wallet.objects.filter(pk__in=selected)

            for wallet in wallets:
                wallet.refresh_from_db()  # ensures latest value
                wallet.add_btc(amount)   # ✅ ADD (not replace)

            messages.success(request, f"{amount} BTC added successfully")

            return redirect(request.get_full_path())

    # 🔥 First time (show form)
    else:
        form = AddBTCForm(initial={
            "_selected_action": request.POST.getlist(ACTION_CHECKBOX_NAME)
        })

    return render(request, "admin/add_btc.html", {
        "wallets": queryset,
        "form": form,
        "action_checkbox_name": ACTION_CHECKBOX_NAME,
    })


# ✅ ADMIN PANEL
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