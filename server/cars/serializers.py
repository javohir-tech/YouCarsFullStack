import re
from datetime import date

# ///////////////// djnago //////////////////////
from django.core.validators import FileExtensionValidator

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
    """
    MOSHINAlarni qoshish
    """

    author = serializers.CharField(read_only=True)
    avto_type = serializers.UUIDField(write_only=True)
    marka = serializers.UUIDField()
    car_model = serializers.UUIDField()
    country = serializers.UUIDField()
    color = serializers.UUIDField()
    fuel = serializers.UUIDField()
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

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["car_model"] = CarModel.objects.get(
            id=validated_data.pop("car_model")
        )
        validated_data["author"] = user
        return Car.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "car_model" in validated_data:
            instance.car_model = CarModel.objects.get(
                id=validated_data.pop("car_model")
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["id"] = instance.id
        data["fullname"] = f"{instance.marka} {instance.car_model}"
        return data

    def validate(self, data):
        auto_type_id = data.get("avto_type" , None)
        marka_id = data.get("marka" , None)
        model_id = data.get("car_model" , None)

        auto_type = AvtoTypeMarka.objects.filter(
            avto_type_id=auto_type_id, marka_id=marka_id
        )

        if not auto_type.exists():
            raise serializers.ValidationError(
                "this car brand does not exist in this vehicle type"
            )

        car_model = CarModel.objects.filter(id=model_id, marka_id=marka_id)

        if not car_model.exists():
            raise serializers.ValidationError(
                "this type of car does not exist in this brand"
            )

        return data

    def validate_avto_type(self, value):
        avto_type = AvtoMobileType.objects.filter(id=value)
        if not avto_type.exists():
            raise serializers.ValidationError("such vehicle type not found")
        value = avto_type.first()
        return value

    def validate_marka(self, value):
        marka = Marka.objects.filter(id=value)
        if not marka.exists():
            raise serializers.ValidationError("such brand not found")
        value = marka.first()
        return value

    def validate_car_model(self, value):
        if not CarModel.objects.filter(id=value).exists():
            raise serializers.ValidationError("such model not found")
        return value

    def validate_country(self, value):
        country = Country.objects.filter(id=value)
        if not country.exists():
            raise serializers.ValidationError("such country not found")
        value = country.first()
        return value

    def validate_color(self, value):
        color = Color.objects.filter(id=value)
        if not color.exists():
            raise serializers.ValidationError("such color not found")

        value = color.first()
        return value

    def validate_fuel(self, value):
        fuel = Fuel.objects.filter(id=value)
        if not fuel.exists():
            raise serializers.ValidationError("such fuel type not found")
        value = fuel.first()
        return value

    def validate_price(self, value):
        if value <= 0 or value > 999999999:
            raise serializers.ValidationError("price must be between 0 and 999999999")

        return value

    def validate_year(self, value):
        current_year = date.today().year

        if value < 1951:
            raise serializers.ValidationError("enter cars manufactured after 1950")

        if value > current_year:
            raise serializers.ValidationError(
                "cannot specify a year greater than the current year"
            )

        return value

    def validate_milage(self, value):

        if value < 0 or value > 2000000:
            raise serializers.ValidationError("mileage must be between 0 and 2 million")

        return value

    def validate_power(self, value):
        if value < 0 or value > 2000:
            raise serializers.ValidationError("horsepower must be between 0 and 2000")
        return value

    def validate_doors_count(self, value):
        if value > 5 or value < 0:
            raise serializers.ValidationError("you can select up to 5 doors")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "you are required to leave a description of at least 10 characters"
            )
        elif len(value) > 1200:
            raise serializers.ValidationError(
                "number of characters must not exceed 1200"
            )

        return value

    def validate_drive_type(self, value):
        if value not in Car.DRIVE_TYPES.values:
            raise serializers.ValidationError(
                "you have entered the drive type incorrectly"
            )

        return value

    def validate_transmission_type(self, value):
        if value not in Car.TRANSMISSION_CHOICES.values:
            raise serializers.ValidationError("such transmission type does not exist")

        return value

    def validate_doors_count(self, value):
        if value not in Car.DOORS_COUNT.values:
            raise serializers.ValidationError("number of doors is incorrect")

        return value

    def validate_body(self, value):
        if value not in Car.BODY_CHOICES.values:
            raise serializers.ValidationError(
                "you have entered the body type incorrectly"
            )

        return value

    def validate_condition(self, value):
        if value not in Car.CONDITION_CHOICES.values:
            raise serializers.ValidationError(
                "you have entered the car condition incorrectly"
            )

        return value

    def validate_availability(self, value):
        if value not in Car.AVAILABILITY_CHOICES.values:
            raise serializers.ValidationError(
                "you have entered the sale status incorrectly"
            )

        return value

    def validate_status(self, value):
        if value not in Car.STATUS_CHOICES.values:
            raise serializers.ValidationError(
                "you have entered the car status incorrectly"
            )

        return value


# /////////////////////////////////////////////////////////
# ////////////   UPLOAD CAR IMAGE      ////////////////////
# /////////////////////////////////////////////////////////
class CarImageUploadSerializer(serializers.Serializer):
    """
    Rasmlarni qoshish
    """

    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    image = serializers.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "jpg", "png", "heic", "heif"]
            )
        ],
    )
    is_main = serializers.BooleanField()
    order = serializers.IntegerField(read_only=True)

    def validate_is_main(self, value):
        car_image = CarImage.objects.filter(is_main=True)
        if car_image and value == True:
            car_image.first().is_main = False
            car_image.first().save()

        return value

    def create(self, validated_data):
        car_image = CarImage.objects.filter(car=validated_data["car"])
        if car_image.exists():
            validated_data["order"] = car_image.last().order + 1
        return CarImage.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr , value in validated_data.items():
            setattr(instance , attr , value)
            
        instance.save()
        return instance


# /////////////////////////////////////////////////////////
# ////////////       GET CAR Images        //////////////////
# /////////////////////////////////////////////////////////
class GetCarImagesSerializer(serializers.ModelSerializer):
    """
    rasmlarni olish
    """

    class Meta:
        model = CarImage
        fields = ["id","image", "is_main", "order"]


# /////////////////////////////////////////////////////////
# ////////////       GET CAR        ///////////////////////
# /////////////////////////////////////////////////////////
class GetCarSerializer(serializers.ModelSerializer):
    """
    Moshinani olish
    """

    author = serializers.StringRelatedField()
    marka = serializers.StringRelatedField()
    avto_type = serializers.StringRelatedField()
    car_model = serializers.StringRelatedField()
    country = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    fuel = serializers.StringRelatedField()
   

    class Meta:
        model = Car
        fields = "__all__"


# /////////////////////////////////////////////////////////
# ////////////       GET ALL CARS        //////////////////
# /////////////////////////////////////////////////////////
class GetCarsSerializer(serializers.ModelSerializer):
    """
        hamma moshinlarni olish
    """
    marka = serializers.StringRelatedField()
    car_model = serializers.StringRelatedField()
    country = serializers.StringRelatedField()
    fuel = serializers.StringRelatedField()
    images = GetCarImagesSerializer(many=True)
    author = serializers.StringRelatedField()
    class Meta:
        model = Car
        fields = [
            "id",
            "author",
            "marka",
            "car_model",
            "year",
            "price",
            "milage",
            "transmission_type",
            "displacement",
            "power",
            "fuel",
            "drive_type",
            "country",
            "status",
            "images",
        ]
