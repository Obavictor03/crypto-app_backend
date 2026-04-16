from django.urls import path
from .views import DepositBTCView, WithdrawBTCView, TransactionListView

urlpatterns = [
    path('deposit/', DepositBTCView.as_view(), name='deposit-btc'),
    path('withdraw/', WithdrawBTCView.as_view(), name='withdraw-btc'),
    path('history/', TransactionListView.as_view(), name='transaction-list'),
]