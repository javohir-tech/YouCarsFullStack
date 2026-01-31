from django.shortcuts import render

# //////////////// REST FRAMEWORK ////////////////
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status

# ///////////////////// MODELS //////////////////////////
from .models import AvtoMobileType, Color, Country, Fuel, Car, CarImage

# //////////// SERIALIZERS  /////////////////////////////
from .serializers import (
    GetAvtoTypeSerializer,
    GetMarkaWithTypeSerializer,
    AvtoTypeMarkaSerializer,
    GetModelsWithMarkaSerializer,
    CarModelSerializer,
    GetColorSerializer,
    GetCountriesSerializer,
    GetFuelSerializer,
    AddCarSerializer,
    CarImageUploadSerializer,
)


# ///////////////////////////////////////////////////////
# ////////////// GET ATVTO TYPE        //////////////////
# ///////////////////////////////////////////////////////
class GetAvtoTypesView(ListAPIView):
    """
    AVTOBAMIL turlarini olish : (yengil , og'ir , moto)
    """

    permission_classes = [IsAuthenticated]
    queryset = AvtoMobileType.objects.all()
    serializer_class = GetAvtoTypeSerializer


# /////////////////////////////////////////////////////////
# //////////// GET MARKA WITH TYPE    /////////////////////
# /////////////////////////////////////////////////////////
class GetMarkaWithTypeView(APIView):
    """
    AVTOMABIL turiga qarab markalarini olish
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GetMarkaWithTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        type_and_markas = serializer.validated_data["markas_and_types"]
        output = AvtoTypeMarkaSerializer(type_and_markas, many=True)

        return Response(
            {
                "success": True,
                "message": "Brands have been received",
                "data": output.data,
            }
        )


# /////////////////////////////////////////////////////////
# //////////// GET MODELS WITH MARKA    ///////////////////
# /////////////////////////////////////////////////////////
class GetModelsWithMarkaView(APIView):
    """
    markaga oid modellarni olish
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = GetModelsWithMarkaSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        car_models = serializer.validated_data.get("car_models")

        car_models_serializer = CarModelSerializer(car_models, many=True)

        return Response(
            {
                "success": True,
                "message": "modellar olindi",
                "models": car_models_serializer.data,
            }
        )


# /////////////////////////////////////////////////////////
# //////////// GET COLORS     /////////////////////////////
# /////////////////////////////////////////////////////////
class GetColorsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Color.objects.all()
    serializer_class = GetColorSerializer


# /////////////////////////////////////////////////////////
# //////////// GET COUNTRY     ////////////////////////////
# /////////////////////////////////////////////////////////
class GetCountriesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetCountriesSerializer
    queryset = Country.objects.all()


# /////////////////////////////////////////////////////////
# //////////// GET COUNTRY     ////////////////////////////
# /////////////////////////////////////////////////////////
class GetFuelsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetFuelSerializer
    queryset = Fuel.objects.all()


# /////////////////////////////////////////////////////////
# ////////////    ADD CAR      ////////////////////////////
# /////////////////////////////////////////////////////////
class AddCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCarSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "success": True,
            "message": "moshina muvvaqiyatli yaratildi",
            "data": serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)


# /////////////////////////////////////////////////////////
# ////////////   UPLOAD CAR IMAGE      ////////////////////
# /////////////////////////////////////////////////////////
class UploadCarImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CarImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"success": True, "message": "rasmlar yuklandi", "data": serializer.data}

        return Response(data, status=status.HTTP_200_OK)
