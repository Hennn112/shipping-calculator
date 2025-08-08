from django.core.management.base import BaseCommand
from core.models import Country, Category

class Command(BaseCommand):
    help = 'Seed initial data for Country and Category'

    def handle(self, *args, **options):
        # Clear existing data
        Category.objects.all().delete()
        Country.objects.all().delete()

        self.stdout.write("Seeding data...")

        # Create Countries
        countries_data = [
            {"country_name": "China", "country_flag": "https://flagcdn.com/w320/cn.png", "country_currency": "CNY"},
            {"country_name": "Thailand", "country_flag": "https://flagcdn.com/w320/th.png", "country_currency": "THB"},
            {"country_name": "Singapore", "country_flag": "https://flagcdn.com/w320/sg.png", "country_currency": "SGD"},
            {"country_name": "Indonesia", "country_flag": "https://flagcdn.com/w320/id.png", "country_currency": "IDR"},
            {"country_name": "Malaysia", "country_flag": "https://flagcdn.com/w320/my.png", "country_currency": "MYR"},
        ]


        countries = {}
        for data in countries_data:
            country = Country.objects.create(**data)
            countries[data["country_name"]] = country

        # Create Categories
        categories_data = [
            {"country": countries["China"], "category_title": "Electronic", "price_per_kilo": 250000},
            {"country": countries["China"], "category_title": "Chip", "price_per_kilo": 300000},
            {"country": countries["China"], "category_title": "Laptop and Computer", "price_per_kilo": 220000},
            {"country": countries["Thailand"], "category_title": "Garments", "price_per_kilo": 200000},
            {"country": countries["Singapore"], "category_title": "Spare parts", "price_per_kilo": 210000},
            {"country": countries["Indonesia"], "category_title": "Furniture", "price_per_kilo": 180000},
            {"country": countries["Indonesia"], "category_title": "Textile", "price_per_kilo": 170000},
            {"country": countries["Malaysia"], "category_title": "Automotive", "price_per_kilo": 230000},
            {"country": countries["Malaysia"], "category_title": "Cosmetics", "price_per_kilo": 190000},
            {"country": countries["Singapore"], "category_title": "Medical Equipment", "price_per_kilo": 280000},
        ]

        for data in categories_data:
            Category.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Successfully seeded Country and Category data."))
