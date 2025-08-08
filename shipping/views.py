from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework import filters
from decimal import Decimal

import requests
from django.conf import settings
from core.serializers import CountrySerializer,CategorySerializer
from core.models import Country, Category

class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['country_name']

class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category_title']

    def get_queryset(self):
        country_id = self.request.query_params.get('country_id')
        queryset = Category.objects.all()

        if country_id:
            queryset = queryset.filter(country_id=country_id)

        return queryset

class ShippingCalculatorAPIView(APIView):
    def get(self, request, *args, **kwargs):
        country_id = request.query_params.get("country_id","")
        category_id = request.query_params.get("category_id","")
        weight = request.query_params.get("weight","")
        destination_subdistrict_id = request.query_params.get("destination_subdistrict_id","")

        # Validasi input
        if not all([country_id, category_id, weight, destination_subdistrict_id]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            country = Country.objects.get(id=country_id)
            category = Category.objects.get(id=category_id, country_id=country_id)
        except Country.DoesNotExist:
            return Response({"error": "Country not found."}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({"error": "Category not found for this country."}, status=status.HTTP_404_NOT_FOUND)

        try:
            weight = Decimal(weight)  # API expects Float or Decimal
        except (ValueError, TypeError):
            return Response({"error": "Invalid weight format."}, status=status.HTTP_400_BAD_REQUEST)

        # Call Komerce Collaborator API /calculate
        url = "https://api-sandbox.collaborator.komerce.id/tariff/api/v1/calculate"
        headers = {
            "accept": "application/json",
            "x-api-key": settings.KOMSHIP_API_KEY
        }
        params = {
            "shipper_destination_id": 8393,
            "receiver_destination_id": destination_subdistrict_id,
            "weight": weight,
            "item_value": 1
        }

        domestic_price = Decimal("0")
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data and data.get("data"):
                services = data["data"].get("calculate_reguler", []) + data["data"].get("calculate_cargo", []) + data["data"].get("calculate_instant", [])

                if not services:
                    return Response({"error": "No shipping services found."}, status=status.HTTP_400_BAD_REQUEST)

                # Ambil grandtotal paling murah
                min_grandtotal = min(Decimal(str(service["grandtotal"])) for service in services)
                domestic_price = min_grandtotal
            else:
                return Response({"error": "Failed to get domestic price from API."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Error connecting to domestic API.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Hitung international price
        international_price = category.price_per_kilo * Decimal(weight)
        total_price = international_price + domestic_price

        return Response({
            "origin": country.country_name,
            "category_name": category.category_title,
            "international_price": str(int(international_price)),
            "domestic_price": str(domestic_price),
            "total_price": str(int(total_price))
        }, status=status.HTTP_200_OK)

class DestinationSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get("keyword", "")
        if not keyword:
            return Response({"error": "keyword parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://api-sandbox.collaborator.komerce.id/tariff/api/v1/destination/search"
        headers = {
            "accept": "application/json",
            "x-api-key": settings.KOMSHIP_API_KEY
        }
        params = {"keyword": keyword}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Failed to fetch destination",
                "details": response.text
            }, status=response.status_code)