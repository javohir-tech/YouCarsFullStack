# //////////////////// REST FRAMEWORK /////////////////
from rest_framework import serializers
from rest_framework.validators import ValidationError

# ////////////////// MODELS //////////////////////////
from .models import AvtoMobileType, AvtoTypeMarka , Marka


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
                {"marka": "An error occurred while fetching brands for this type of vehicle."}
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
        
        
    

