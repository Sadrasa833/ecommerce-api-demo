from django.urls import path
from .views import StockSummaryView, StockMovementsView

urlpatterns = [
    path("summary/", StockSummaryView.as_view(), name="stock-summary"),
    path("movements/", StockMovementsView.as_view(), name="stock-movements"),
]
