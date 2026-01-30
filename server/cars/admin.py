from django.contrib import admin

# MODELS
from .models import Marka, CarModel, Color, Country, Fuel, Car, CarImage


@admin.register(Marka)
class MarkaAdmin(admin.ModelAdmin):
    list_display = ["marka", "photo", "id"]
    search_fields = ["marka"]
    list_filter = ["created_time", "updated_time"]
    ordering = ["marka"]
    list_per_page = 20


@admin.register(CarModel)
class CarModel(admin.ModelAdmin):
    list_display = ["name", "marka", "id"]
    search_fields = ["name"]
    list_filter = ["created_time", "updated_time", "marka"]
    ordering = ["name"]
    list_per_page = 20


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["color", "color_code", "id"]
    search_fields = ["color"]
    ordering = ["color"]
    list_per_page = 20


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["country", "flag", "id"]
    search_fields = ["country"]
    ordering = ["country"]
    list_per_page = 10


@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    ordering = ["name"]
    list_per_page = 10


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "car_model", "marka", "body" , "availability"]
    list_filter = [
        "car_model",
        "marka",
        "author",
        "country",
        "color",
        "fuel",
        "drive_type",
        "transmission_type",
        "body", 
        "availability", 
        "year",
        "price"
    ]
    list_per_page = 20
    


# Register your models here.
