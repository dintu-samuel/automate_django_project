from django.urls import path
from . import views

urlpatterns = [
    path('stocks/',views.stocks, name='stocks'),
    path('stock_autocomplete/',views.StockAutocomplete.as_view(), name='stock-autocomplete'),
    path('stock_detail/<int:pk>/',views.stock_detail, name='stock_detail'),
]
