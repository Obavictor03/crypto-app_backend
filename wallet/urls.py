from django.urls import path
from .views import BTCPriceView, WalletView

urlpatterns = [
    path('btc-price/', BTCPriceView.as_view(), name='btc-price'),
    path('wallet/', WalletView.as_view(), name='wallet'),
]