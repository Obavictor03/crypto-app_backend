from django.contrib import admin
from .models import Wallet
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME

class AddBTCForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    amount = forms.FloatField(label="BTC Amount", min_value=0.00000001)

@admin.action(description="Add BTC")
def add_btc(modeladmin, request, queryset):

    # ✅ STEP 1: If user clicked "Apply" → process form
    if request.POST.get("apply"):
        form = AddBTCForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            selected = request.POST.getlist(ACTION_CHECKBOX_NAME)
            wallets = queryset

            for wallet in wallets:
                wallet.add_btc(amount)

            messages.success(request, f"{amount} BTC added successfully")

            return redirect(request.get_full_path())

    # ✅ STEP 2: First time → show form
    else:
        form = AddBTCForm(initial={
            "_selected_action": request.POST.getlist(ACTION_CHECKBOX_NAME)
        })


    return render(request, "admin/add_btc.html", {
        "wallets": queryset,
        "form": form,
        "action_checkbox_name": ACTION_CHECKBOX_NAME,
    })

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "btc_balance", "get_balance")
    readonly_fields = ("get_balance",)
    actions = [add_btc]

    def get_balance(self, obj):
        return obj.balance

    def has_add_permission(self, request):
        return False