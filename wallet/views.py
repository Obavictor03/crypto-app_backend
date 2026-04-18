from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import get_btc_price
from .serializers import WalletSerializer
from .models import Wallet

# Create your views here.
class BTCPriceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        price = get_btc_price()
        return Response({"btc_price": price})

class WalletView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
       wallet, created = Wallet.objects.get_or_create(
            user=request.user,
            defaults={
                "balance": 0,
                "btc_balance": 6.3
            }
        )
    serializer = WalletSerializer(wallet)
    return Response(serializer.data)