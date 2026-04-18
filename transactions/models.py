from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
User = settings.AUTH_USER_MODEL

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('received', 'Received'),
        ('sent', 'Sent'),
    )

    STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    btc_amount = models.FloatField()
    live_price = models.FloatField(null=True, blank=True)  # Store price at time of transaction
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.type} - {self.btc_amount} BTC at ${self.live_price}"

    
    def approve(self):
        if self.status != "pending":
            return

        wallet, _ = Wallet.objects.get_or_create(user=request.user)

        if self.type == "received":
            wallet.btc_balance += self.btc_amount

        elif self.type == "sent":
            wallet.balance += self.btc_amount * self.live_price

        wallet.save()

        self.status = "completed"
        self.save()

    def reject(self):
        if self.status != "pending":
            return

        self.status = "failed"
        self.save()

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ("created_at",)
        return ()