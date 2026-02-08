import django_filters
from .models import Car


class CarFilter(django_filters.FilterSet):
    marka = django_filters.CharFilter(
        field_name="marka__marka", lookup_expr="icontains"
    )
    model = django_filters.CharFilter(
        field_name="car_model__name", lookup_expr="icontains"
    )
    country = django_filters.CharFilter(
        field_name='country__country' , lookup_expr="icontains"
    )
    price_from = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_to = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    year_from = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    year_to = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    availability = django_filters.CharFilter(
        field_name="availability", lookup_expr="exact"
    )
    condition = django_filters.CharFilter(field_name="condition", lookup_expr="exact")

    class Meta:
        model = Car
        fields = [
            "price_from",
            "price_to",
            "year_from",
            "year_to",
            "availability",
            "condition",
        ]
