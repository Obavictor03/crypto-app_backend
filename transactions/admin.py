from django.contrib import admin
from .models import Transaction
# Register your models here.


@admin.action(description="Approve selected transactions")
def approve_transactions(modeladmin, request, queryset):
    for tx in queryset:
        tx.approve()

@admin.action(description="Reject selected transactions")
def reject_transactions(modeladmin, request, queryset):
    for tx in queryset:
        tx.reject()


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "status", "btc_amount", "created_at")
    list_filter = ("status", "type")
    actions = [approve_transactions, reject_transactions]

    fields = ("user", "type", "status", "btc_amount", "created_at")