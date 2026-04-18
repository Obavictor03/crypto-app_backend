from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from .models import Transaction
from wallet.utils import get_btc_price
from wallet.models import Wallet

# Create your views here.

# Deposit BTC Logic
class DepositBTCView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = float(request.data.get("amount"))

        wallet, _ = Wallet.objects.get_or_create(user=request.user)

        if wallet.balance < amount:
            return Response(
                {"error": "Insufficient funds"},
                status=400
            )

        price = get_btc_price()
        btc_amount = amount / price

        # ✅ Update wallet
        wallet.balance -= amount
        wallet.save()


        # Only create transaction (NO wallet update)
        Transaction.objects.create(
            user=request.user,
            type="received",
            status="pending",  
            btc_amount=btc_amount, 
            live_price=price,
        )

        return Response({
            "message": "Buy request submitted. Awaiting confirmation."
        })

# Withdraw BTC Logic

class WithdrawBTCView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        btc_amount = request.data.get("btc_amount")

        if not btc_amount:
            return Response(
                {"error": "btc_amount is required"},
                status=400
            )

        try:
            btc_amount = float(btc_amount)
        except ValueError:
            return Response(
                {"error": "Invalid BTC amount"},
                status=400
            )

        wallet, _ = Wallet.objects.get_or_create(user=request.user)

        if wallet.btc_balance < btc_amount:
            return Response(
                {"error": "Insufficient BTC"},
                status=400
            )

        price = get_btc_price()
        usd_value = btc_amount * price

        # ✅ Update wallet
        wallet.btc_balance -= btc_amount
        wallet.save()

        # ✅ Save transaction
        Transaction.objects.create(
            user=request.user,
            type="sent",
            status="pending",
            btc_amount=btc_amount,
            live_price=price
        )

        return Response({"message": "Withdraw successful"})

# Transaction History API
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

class TransactionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')