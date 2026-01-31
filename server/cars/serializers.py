import re
from datetime import date

# //////////////////// REST FRAMEWORK /////////////////
from rest_framework import serializers
from rest_framework.validators import ValidationError

# ////////////////// MODELS //////////////////////////
from .models import (
    AvtoMobileType,
    AvtoTypeMarka,
    Marka,
    CarModel,
    Color,
    Country,
    Fuel,
    Car,
    CarImage,
)


# ///////////////////////////////////////////////////////
# ////// GET ATVTO TYPE SERIALIZER     //////////////////
# ///////////////////////////////////////////////////////
class GetAvtoTypeSerializer(serializers.ModelSerializer):
    """
    AVTOMABIL turlarini olish
    """

    class Meta:
        model = AvtoMobileType
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]


# /////////////////////////////////////////////////////////
# //////////// GET MARKA WITH TYPE    /////////////////////
# /////////////////////////////////////////////////////////
class GetMarkaWithTypeSerializer(serializers.Serializer):
    """
    AVTOMABIL turlariga kora markalarni olish
    """

    avto_type = serializers.CharField(max_length=2, required=True, write_only=True)
    markas = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        avto_type = data.get("avto_type")

        temp_type = AvtoMobileType.objects.filter(name=avto_type).first()

        if temp_type is None:
            raise ValidationError({"type": "This type of vehicle does not exist."})

        markas_and_types = AvtoTypeMarka.objects.filter(avto_type=temp_type)

        if not markas_and_types.exists():
            raise ValidationError(
                {
                    "marka": "An error occurred while fetching brands for this type of vehicle."
                }
            )

        data["markas_and_types"] = markas_and_types

        return data


# /////////////////////////////////////////////////////////
# //////////// AVTo TYPE MARKA SERIALIZER    //////////////
# /////////////////////////////////////////////////////////
class AvtoTypeMarkaSerializer(serializers.ModelSerializer):
    """
    AVTOMABIL turlariga kora markalarni malumotlarini olish
    """

    id = serializers.UUIDField(source="marka.id")
    marka = serializers.CharField(source="marka.marka")
    photo = serializers.ImageField(source="marka.photo")

    class Meta:
        model = AvtoTypeMarka
        fields = ["id", "marka", "photo"]


# /////////////////////////////////////////////////////////
# //////////// GET MODELS WITH MARKA    ///////////////////
# /////////////////////////////////////////////////////////
class GetModelsWithMarkaSerializer(serializers.Serializer):
    """
    markaga oid modellarni olish
    """

    marka_id = serializers.UUIDField(write_only=True)

    def validate(self, data):
        marka_id = data.get("marka_id")

        marka = Marka.objects.filter(id=marka_id)

        if not marka.exists():
            raise ValidationError({"marka": "bunday marka topilmadi"})

        car_models = CarModel.objects.filter(marka=marka.first())

        if not car_models.exists():
            raise ValidationError(
                {"car_models": f"{marka.first().marka} ga oid modellar topilmadi"}
            )

        data["car_models"] = car_models

        return data


class CarModelSerializer(serializers.ModelSerializer):
    """
    Modellarni serializer qilish
    """

    class Meta:
        model = CarModel
        fields = ["id", "name"]


# /////////////////////////////////////////////////////////
# //////////// GET COLORS     /////////////////////////////
# /////////////////////////////////////////////////////////
class GetColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ["id", "color", "color_code"]


# /////////////////////////////////////////////////////////
# //////////// GET COUNTRY     ////////////////////////////
# /////////////////////////////////////////////////////////
class GetCountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ["id", "country"]


# /////////////////////////////////////////////////////////
# //////////// GET FUEL        ////////////////////////////
# /////////////////////////////////////////////////////////
class GetFuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        fields = ["id", "name"]


# /////////////////////////////////////////////////////////
# ////////////    ADD CAR      ////////////////////////////
# /////////////////////////////////////////////////////////
class AddCarSerializer(serializers.Serializer):
    auto_type_id = serializers.UUIDField(write_only=True)
    marka_id = serializers.UUIDField()
    model_id = serializers.UUIDField()
    country_id = serializers.UUIDField()
    color_id = serializers.UUIDField()
    fuel_id = serializers.UUIDField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    year = serializers.IntegerField()
    milage = serializers.IntegerField()
    displacement = serializers.DecimalField(max_digits=2, decimal_places=1)
    power = serializers.IntegerField()
    drive_type = serializers.CharField(max_length=3)
    transmission_type = serializers.CharField(max_length=2)
    doors_count = serializers.IntegerField()
    description = serializers.CharField(max_length=1200)
    body = serializers.CharField()
    condition = serializers.CharField(max_length=10)
    availability = serializers.CharField(max_length=10)
    status = serializers.CharField(max_length=2)

    def validate(self, data):
        auto_type_id = data.get("auto_type_id")
        marka_id = data.get("marka_id")
        model_id = data.get("model_id")

        auto_type = AvtoTypeMarka.objects.filter(
            avto_type_id=auto_type_id, marka_id=marka_id
        )

        if not auto_type.exists():
            raise serializers.ValidationError(
                "ushbu avtomabil turida quyidagi avtomail markasi mavjud emas"
            )

        car_model = CarModel.objects.filter(id=model_id, marka_id=marka_id)

        if not car_model.exists():
            raise serializers.ValidationError(
                "ushbu markada bu turdagi avtomabil mavjud emas"
            )

        return data

    def validate_auto_type_id(self, value):
        if not AvtoMobileType.objects.filter(id=value).exists():
            raise serializers.ValidationError("bunday transport turi topilmadi")
        return value

    def validate_marka_id(self, value):
        if not Marka.objects.filter(id=value).exists():
            raise serializers.ValidationError("bunday marka topilmadi")
        return value

    def validate_model_id(self, value):
        if not CarModel.objects.filter(id=value).exists():
            raise serializers.ValidationError("bunday model topilmadi")
        return value

    def validate_country_id(self, value):
        if not Country.objects.filter(id=value).exists():
            raise serializers.ValidationError("bunday davlat topilmadi")
        return value

    def validate_color_id(self, value):
        if not Color.objects.filter(id=value).exists():
            raise serializers.ValidationError("bunday rang topilmadi")

        return value

    def validate_fuel_id(self, value):
        if not Fuel.objects.filter(id=value).exists():
            raise serializers.ValidationError("bunday yoqilgi turi topilmadi")

        return value

    def validate_price(self, value):
        if value <= 0 or value > 999999999:
            raise serializers.ValidationError(
                "narxa 0 va 999999999 orasida bolishi kerak"
            )

        return value

    def validate_year(self, value):
        current_year = date.today().year

        if value < 1951:
            raise serializers.ValidationError(
                "1950 yildan keyin ishlab chiqarilgan mashinalarni kiriting"
            )

        if value > current_year:
            raise serializers.ValidationError(
                "Hozirgi yildan katta bo‘lgan yilni belgilash mumkin emas"
            )

        return value

    def validate_milage(self, value):

        if value < 0 or value > 2000000:
            raise serializers.ValidationError(
                "yurgan masofa 0 va 2 mln oraasida bolishi kerak"
            )

        return value

    def validate_power(self, value):
        if value < 0 or value > 2000:
            raise serializers.ValidationError(
                "ot kukichini 0 va 2000 orasida bolshi kerak"
            )
        return value

    def validate_doors_count(self, value):
        if value > 5 or value < 0:
            raise serializers.ValidationError("5 taga eshik tanlashingi mumkin")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "kamida 10  ta belgidan iborat sharx qoldirip ketishingiz talap etiladi "
            )
        elif len(value) > 1200:
            raise serializers.ValidationError("belgilar soni 1200 dan oshmasligi kerak")

        return value

    def validate_drive_type(self, value):
        if value not in Car.DRIVE_TYPES.values:
            raise serializers.ValidationError(
                "moshina balonlar ishlash tartibini hato kiritgansiz"
            )

        return value

    def validate_transmission_type(self, value):
        if value not in Car.TRANSMISSION_CHOICES.values:
            raise serializers.ValidationError("bunday uztma turi mavjud emas")

        return value

    def validate_doors_count(self, value):
        if value not in Car.DOORS_COUNT.values:
            raise serializers.ValidationError("eshiklar soni hato")

        return value

    def validate_body(self, value):
        if value not in Car.BODY_CHOICES.values:
            raise serializers.ValidationError("kuzzovni hato kiritgansiz")

        return value

    def validate_condition(self, value):
        if value not in Car.CONDITION_CHOICES.values:
            raise serializers.ValidationError("moshina holatini hato kiritgansiz")

        return value

    def validate_availability(self, value):
        if value not in Car.AVAILABILITY_CHOICES.values:
            raise serializers.ValidationError("savdo holatini hato kiritgansiz")

        return value

    def validate_status(self, value):
        if value not in Car.STATUS_CHOICES.values:
            raise serializers.ValidationError("moshina statusini hoto kirtgansiz")

        return value
