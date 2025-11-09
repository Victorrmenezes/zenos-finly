from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    CreditCardsListView,
    TransactionViewSet,
    CategoryViewSet,
    CreditCardTransactionsView,
    AccountsSummaryView,
    CreditCardImportView,
)

router = DefaultRouter()
router.register(r"transactions", TransactionViewSet, basename="transaction")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
    path("credit-cards/transactions/", CreditCardTransactionsView.as_view(), name="credit_card_transactions"),
    path("credit-cards/import/", CreditCardImportView.as_view(), name="credit_card_import"),
    path("accounts/summary/", AccountsSummaryView.as_view(), name="accounts_summary"),
    path("credit-cards/", CreditCardsListView.as_view(), name="credit_cards_list"),
]
