from django.contrib import admin
from .models import Wallet
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages

class AddBTCForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    amount = forms.FloatField(label="BTC Amount", min_value=0.00000001)

@admin.action(description="Add BTC (custom amount)")
def add_btc(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = AddBTCForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            for wallet in queryset:
                wallet.add_btc(amount)

            messages.success(request, f"{amount} BTC added successfully")
            return redirect(request.get_full_path())

    else:
        form = AddBTCForm(initial={
            '_selected_action': request.POST.getlist('_selected_action')
        })

    return render(request, "admin/add_btc.html", {
        "wallets": queryset,
        "form": form,
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