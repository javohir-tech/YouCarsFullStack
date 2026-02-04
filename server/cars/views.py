from django.shortcuts import render

# //////////////// REST FRAMEWORK ////////////////
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

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
    GetCarsSerializer,
    GetCarSerializer,
    GetCarImagesSerializer,
)

# ///////////// PAGINATORS ////////////////////
from shared.custom_pagination import CustomPagination


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
class CarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCarSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "success": True,
            "message": "moshina muvvaqiyatli yaratildi",
            "data": {"id": serializer.data.get("id")},
        }

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        serializer = AddCarSerializer(car, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "o'zgartirildi",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        serializer = AddCarSerializer(car, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "patch ishladi",
                "data": serializer.data,
            }
        )

    def delete(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        car.delete()

        return Response(
            {
                "success": True,
                "message": "ochirildi",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def get(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        carSerializer = GetCarSerializer(car)
        images = CarImage.objects.filter(car=car)
        images_data = GetCarImagesSerializer(images, many=True)
        car_data = carSerializer.data.copy()
        car_data["images"] = images_data.data
        data = {
            "success": True,
            "message": "yuklandi",
            "data": car_data,
        }
        return Response(data)


# /////////////////////////////////////////////////////////
# //////////// UPLOAD and CHANGE CAR IMAGE/////////////////
# /////////////////////////////////////////////////////////
class UploadCarImageView(APIView):
    """
    moshina rasmlarini joylash
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CarImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "success": True,
            "message": "rasmlar yuklandi",
            "data": serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        car_image = get_object_or_404(CarImage, car_id=pk)
        serializer = CarImageUploadSerializer(car_image, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "ozgardi",
                "data": serializer.data,
            }
        )


# /////////////////////////////////////////////////////////
# ////////////       GET ALL CARS         /////////////////
# /////////////////////////////////////////////////////////
class GetAllCarsView(ListAPIView):
    """
    Hamma moshinalarni olish uchun
    """

    permission_classes = [AllowAny]
    serializer_class = GetCarsSerializer
    queryset = Car.objects.filter(status=Car.STATUS_CHOICES.PUBLISHED)
    pagination_class = CustomPagination


# /////////////////////////////////////////////////////////
# ////////////       GET MY CARS          /////////////////
# /////////////////////////////////////////////////////////
class GetUserCarsFDraftView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetCarsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Car.objects.filter(
            author=self.request.user, status=Car.STATUS_CHOICES.DRAFT
        )


class GetUserCarsPublished(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetCarsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Car.objects.filter(
            author=self.request.user, status=Car.STATUS_CHOICES.PUBLISHED
        )
