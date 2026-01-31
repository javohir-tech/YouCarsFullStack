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
        fields = ["name"]
        read_only_fields = ["name"]


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
