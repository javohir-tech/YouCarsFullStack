from django.contrib import admin

# MODELS
from .models import (
    Marka,
    CarModel,
    Color,
    Country,
    Fuel,
    Car,
    CarImage,
    AvtoMobileType,
    AvtoTypeMarka,
    DeletionStatistics,
    Like, 
)


@admin.register(AvtoMobileType)
class AvtoTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


@admin.register(AvtoTypeMarka)
class AvtoTypeMarkaAdmin(admin.ModelAdmin):
    list_display = ["avto_type", "marka", "id"]
    list_filter = ["avto_type", "marka"]
    search_fields = ["marka"]
    list_per_page = 20


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
    list_display = ["id", "author", "car_model", "marka", "body", "availability"]
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
    ]
    search_fields = ["year", "price", "marka__marka", "car_model__name"]
    list_per_page = 20


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ["car", "image", "is_main", "order"]
    list_filter = ["car", "is_main"]
    list_per_page = 20


@admin.register(DeletionStatistics)
class DeletionStatistics(admin.ModelAdmin):
    list_display = ["sold_on_youcar", "sold_elsewhere", "other_reason"]
    
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['author' , "car"]
    list_filter = ['author' , 'car']
    search_fields = ['author' , 'car']
    list_per_page = 20


# Register your models here.
