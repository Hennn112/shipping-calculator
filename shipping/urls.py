from django.urls import path
from .views import ShippingCalculatorAPIView, CountryListAPIView,CategoryListAPIView,DestinationSearchAPIView

urlpatterns = [
    path('calculate/', ShippingCalculatorAPIView.as_view(), name='shipping-calculate'),
    path('countries/', CountryListAPIView.as_view(), name='country-list'),
    path('categories/', CategoryListAPIView.as_view(), name="category-list"),
    path('destinations/', DestinationSearchAPIView.as_view(), name="destination-search"),
]
