from django.shortcuts import render

# /////////////////////// FILTER ///////////////////////////
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from .filters import CarFilter, GetMarkasWithModelsFilter, GetModelsWithAvtoTypeFilter

# //////////////// REST FRAMEWORK ////////////////
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

# ///////////////////// MODELS //////////////////////////
from .models import (
    AvtoMobileType,
    Color,
    Country,
    Fuel,
    Car,
    CarImage,
    Like,
    DeletionStatistics,
    Marka,
    CarModel,
)

# ////////////////////// Permissions /////////////////////
from .permissions import IsAuthor , IsAuthorImage

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
    CarSerializer,
    CarImageUploadSerializer,
    GetCarsSerializer,
    GetCarSerializer,
    CarDeletionSerializer,
    GetAllMarkasSerializer,
    getAllModelsSerializer,
    GetMarkasWithModels,
)

# ///////////// PAGINATORS ////////////////////
from shared.custom_pagination import CustomPagination

# ////////////////// SWAGGER ///////////////////////
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Avtomobil turiga qarab markalarni olish",
        operation_summary="Marka olish (avto turi bo'yicha)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["avto_type"],
            properties={
                "avto_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Avtomobil turi nomi",
                    example="CT , CR , MO",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Markalar muvaffaqiyatli olindi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Brands have been received",
                        ),
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER, example=1
                                    ),
                                    "marka": openapi.Schema(
                                        type=openapi.TYPE_STRING, example="Toyota"
                                    ),
                                    "logo": openapi.Schema(
                                        type=openapi.TYPE_STRING, format="uri"
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
            400: "Validatsiya xatosi",
            401: "Autentifikatsiya talab qilinadi",
        },
        tags=["Reference Data"],
    )
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

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Marka bo'yicha mashina modellarini olish",
        operation_summary="Modellar olish (marka bo'yicha)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["marka"],
            properties={
                "marka": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Marka nomi", example="Toyota"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Modellar muvaffaqiyatli olindi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="modellar olindi"
                        ),
                        "models": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER, example=1
                                    ),
                                    "name": openapi.Schema(
                                        type=openapi.TYPE_STRING, example="Camry"
                                    ),
                                    "marka": openapi.Schema(
                                        type=openapi.TYPE_STRING, example="Toyota"
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
            400: "Validatsiya xatosi",
            401: "Autentifikatsiya talab qilinadi",
        },
        tags=["Reference Data"],
    )
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
# //////////// GET MARKA WITH MODELS    ///////////////////
# /////////////////////////////////////////////////////////
class GetMarkasWithModelsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = GetMarkasWithModels
    queryset = Marka.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = GetMarkasWithModelsFilter


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
    permission_classes = [AllowAny]
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
# ////////////        CAR      ////////////////////////////
# /////////////////////////////////////////////////////////
class CarView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated() , IsAuthor()]

    @swagger_auto_schema(
        operation_description="Yangi mashina e'lonini yaratish",
        operation_summary="Mashina yaratish",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "avto_type",
                "marka",
                "car_model",
                "country",
                "color",
                "fuel",
                "price",
                "year",
                "milage",
                "displacement",
                "power",
                "drive_type",
                "transmission_type",
                "doors_count",
                "description",
                "body",
                "condition",
                "availability",
                "status",
            ],
            properties={
                "avto_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Avto turi (masalan: sedan, SUV, crossover)",
                    example="sedan",
                ),
                "marka": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Mashina markasi",
                    example="Toyota",
                ),
                "car_model": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Mashina modeli",
                    example="Camry",
                ),
                "country": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Ishlab chiqarilgan mamlakat",
                    example="Japan",
                ),
                "color": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Mashina rangi",
                    example="Qora",
                ),
                "fuel": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Yoqilg'i turi",
                    example="Benzin",
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format="decimal",
                    description="Narxi (0 dan 999999999 gacha)",
                    example=25000.00,
                ),
                "year": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Ishlab chiqarilgan yili (1951 dan hozirgi yilgacha)",
                    example=2020,
                ),
                "milage": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Yurgan masofasi km da (0 dan 2000000 gacha)",
                    example=45000,
                ),
                "displacement": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format="decimal",
                    description="Dvigatel hajmi (litrda)",
                    example=2.5,
                ),
                "power": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Ot kuchi (0 dan 2000 gacha)",
                    example=200,
                ),
                "drive_type": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Yurish turi", example="FWD"
                ),
                "transmission_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Uzatmalar qutisi turi",
                    example="AT",
                ),
                "doors_count": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Eshiklar soni (0 dan 5 gacha)",
                    example=4,
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Tavsif (10 dan 1200 belgigacha)",
                    example="Juda yaxshi holatda, to'liq ehtiyot qismlari yangi",
                ),
                "body": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Kuzov turi", example="Sedan"
                ),
                "condition": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Mashina holati",
                    example="new",
                ),
                "availability": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Sotuvda mavjudligi",
                    example="available",
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="E'lon holati", example="AC"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Mashina muvaffaqiyatli yaratildi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="moshina muvvaqiyatli yaratildi",
                        ),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format="uuid",
                                    example="123e4567-e89b-12d3-a456-426614174000",
                                )
                            },
                        ),
                    },
                ),
            ),
            400: "Validatsiya xatosi",
            401: "Autentifikatsiya talab qilinadi",
        },
        tags=["Car"],
    )
    def post(self, request):
        serializer = CarSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "success": True,
            "message": "moshina muvvaqiyatli yaratildi",
            "data": {"id": serializer.data.get("id")},
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Mashinaning barcha ma'lumotlarini yangilash (to'liq)",
        operation_summary="Mashinani yangilash (PUT)",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Mashina ID (UUID format)",
                type=openapi.TYPE_STRING,
                format="uuid",
                required=True,
                example="123e4567-e89b-12d3-a456-426614174000",
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "avto_type",
                "marka",
                "car_model",
                "country",
                "color",
                "fuel",
                "price",
                "year",
                "milage",
                "displacement",
                "power",
                "drive_type",
                "transmission_type",
                "doors_count",
                "description",
                "body",
                "condition",
                "availability",
                "status",
            ],
            properties={
                "avto_type": openapi.Schema(type=openapi.TYPE_STRING, example="sedan"),
                "marka": openapi.Schema(type=openapi.TYPE_STRING, example="Toyota"),
                "car_model": openapi.Schema(type=openapi.TYPE_STRING, example="Camry"),
                "country": openapi.Schema(type=openapi.TYPE_STRING, example="Japan"),
                "color": openapi.Schema(type=openapi.TYPE_STRING, example="Qora"),
                "fuel": openapi.Schema(type=openapi.TYPE_STRING, example="Benzin"),
                "price": openapi.Schema(type=openapi.TYPE_NUMBER, example=25000.00),
                "year": openapi.Schema(type=openapi.TYPE_INTEGER, example=2020),
                "milage": openapi.Schema(type=openapi.TYPE_INTEGER, example=45000),
                "displacement": openapi.Schema(type=openapi.TYPE_NUMBER, example=2.5),
                "power": openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                "drive_type": openapi.Schema(type=openapi.TYPE_STRING, example="FWD"),
                "transmission_type": openapi.Schema(
                    type=openapi.TYPE_STRING, example="AT"
                ),
                "doors_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=4),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, example="Yaxshi holatda"
                ),
                "body": openapi.Schema(type=openapi.TYPE_STRING, example="Sedan"),
                "condition": openapi.Schema(type=openapi.TYPE_STRING, example="used"),
                "availability": openapi.Schema(
                    type=openapi.TYPE_STRING, example="available"
                ),
                "status": openapi.Schema(type=openapi.TYPE_STRING, example="AC"),
            },
        ),
        responses={
            200: openapi.Response(
                description="Mashina muvaffaqiyatli yangilandi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="o'zgartirildi"
                        ),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
            400: "Validatsiya xatosi",
            401: "Autentifikatsiya talab qilinadi",
            404: "Mashina topilmadi",
        },
        tags=["Car"],
    )
    def put(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        
        self.check_object_permissions(request , car)
        serializer = CarSerializer(car, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "o'zgartirildi",
                "data": serializer.data,
            }
        )

    @swagger_auto_schema(
        operation_description="Mashinaning ayrim ma'lumotlarini yangilash (qisman)",
        operation_summary="Mashinani yangilash (PATCH)",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Mashina ID (UUID format)",
                type=openapi.TYPE_STRING,
                format="uuid",
                required=True,
                example="123e4567-e89b-12d3-a456-426614174000",
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "price": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Yangi narx", example=30000.00
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Yangi tavsif",
                    example="Narx tushirildi",
                ),
                "availability": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Mavjudlik holati",
                    example="available",
                ),
                "marka": openapi.Schema(type=openapi.TYPE_STRING),
                "car_model": openapi.Schema(type=openapi.TYPE_STRING),
                "color": openapi.Schema(type=openapi.TYPE_STRING),
                "year": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            description="Faqat o'zgartirmoqchi bo'lgan fieldlarni yuboring",
        ),
        responses={
            200: openapi.Response(
                description="Mashina qisman yangilandi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="patch ishladi"
                        ),
                    },
                ),
            ),
            400: "Validatsiya xatosi",
            401: "Autentifikatsiya talab qilinadi",
            404: "Mashina topilmadi",
        },
        tags=["Car"],
    )
    def patch(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        
        self.check_object_permissions(request , car)
        serializer = CarSerializer(car, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "patch ishladi",
            }
        )

    @swagger_auto_schema(
        operation_description="Mashinani o'chirish",
        operation_summary="Mashinani o'chirish",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Mashina ID (UUID format)",
                type=openapi.TYPE_STRING,
                format="uuid",
                required=True,
                example="123e4567-e89b-12d3-a456-426614174000",
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["reason"],
            properties={
                "reason": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="O'chirish sababi",
                    example="sotildi",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Mashina muvaffaqiyatli o'chirildi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="ochirildi"
                        ),
                    },
                ),
            ),
            400: "Validatsiya xatosi",
            401: "Autentifikatsiya talab qilinadi",
            404: "Mashina topilmadi",
        },
        tags=["Car"],
    )
    def delete(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        
        self.check_object_permissions(request , car)
        deletion_serializer = CarDeletionSerializer(data=request.data)
        deletion_serializer.is_valid(raise_exception=True)
        reason = deletion_serializer.validated_data["reason"]

        DeletionStatistics.increment_reason(reason)
        car.delete()

        return Response(
            {
                "success": True,
                "message": "ochirildi",
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_description="Bitta mashinaning to'liq ma'lumotlarini olish",
        operation_summary="Mashinani ko'rish",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Mashina ID (UUID format)",
                type=openapi.TYPE_STRING,
                format="uuid",
                required=True,
                example="123e4567-e89b-12d3-a456-426614174000",
            )
        ],
        responses={
            200: openapi.Response(
                description="Mashina ma'lumotlari",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="yuklandi"
                        ),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
            401: "Autentifikatsiya talab qilinadi",
            404: "Mashina topilmadi",
        },
        tags=["Car"],
    )
    def get(self, request, pk):

        car = get_object_or_404(Car, id=pk)
        car.views = car.views + 1
        car.save()
        carSerializer = GetCarSerializer(car, context={"request": request})
        data = {
            "success": True,
            "message": "yuklandi",
            "data": carSerializer.data,
        }
        return Response(data)


# /////////////////////////////////////////////////////////
# //////////// UPLOAD and CHANGE CAR IMAGE/////////////////
# /////////////////////////////////////////////////////////
class CarImageView(APIView):
    """
    moshina rasmlarini joylash
    """

    permission_classes = [IsAuthenticated , IsAuthorImage]

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

    def delete(self, request, pk):
        car_image = get_object_or_404(CarImage, id=pk)
        
        # self.check_object_permissions(request , car_image)
        car_image.delete()
        return Response(
            {
                "success": True,
                "message": "ochirildi",
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
    queryset = Car.objects.filter(status=Car.STATUS_CHOICES.PUBLISHED).order_by(
        "-views"
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter
    pagination_class = CustomPagination


class GetSimilarCarsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = GetCarsSerializer

    def get_queryset(self):
        id = self.kwargs.get("pk")
        car = get_object_or_404(Car, id=id)
        marka = car.marka
        return Car.objects.filter(marka=marka).order_by("-views").exclude(id=id)[:3]


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
        ).order_by("-created_time")


class GetUserCarsPublished(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetCarsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Car.objects.filter(
            author=self.request.user, status=Car.STATUS_CHOICES.PUBLISHED
        ).order_by("-created_time")


# /////////////////////////////////////////////////////////
# ////////////       LIKE AND DISLIKE     /////////////////
# /////////////////////////////////////////////////////////
class LikeAndDislikeView(APIView):
    """
    Mashinani like/unlike qilish
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Mashinani like qilish. Agar avval like bosilgan bo'lsa, xatolik qaytaradi.",
        operation_summary="Mashinani like qilish",
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="Mashina ID (UUID format)",
                type=openapi.TYPE_STRING,
                format="uuid",
                required=True,
                example="123e4567-e89b-12d3-a456-426614174000",
            )
        ],
        responses={
            200: openapi.Response(
                description="Like muvaffaqiyatli qo'shildi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="like bosildi"
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Allaqachon like bosilgan",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "like": openapi.Schema(
                            type=openapi.TYPE_STRING, example="like bosilgan"
                        )
                    },
                ),
            ),
            401: "Autentifikatsiya talab qilinadi",
            404: "Mashina topilmadi",
        },
        tags=["Likes"],
    )
    def post(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        if not Like.objects.filter(author=request.user, car=car).exists():
            Like.objects.create(author=request.user, car=car)
            return Response({"success": True, "message": "like bosildi"})
        else:
            raise ValidationError({"like": "like bosilgan"})

    @swagger_auto_schema(
        operation_description="Mashinadan like ni olib tashlash (unlike)",
        operation_summary="Like ni olib tashlash",
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="Mashina ID (UUID format)",
                type=openapi.TYPE_STRING,
                format="uuid",
                required=True,
                example="123e4567-e89b-12d3-a456-426614174000",
            )
        ],
        responses={
            200: openapi.Response(
                description="Like muvaffaqiyatli olib tashlandi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, example=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="dislike"
                        ),
                    },
                ),
            ),
            401: "Autentifikatsiya talab qilinadi",
            404: openapi.Response(
                description="Mashina yoki like topilmadi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, example="Not found."
                        )
                    },
                ),
            ),
        },
        tags=["Likes"],
    )
    def delete(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        car_like = get_object_or_404(Like, author=request.user, car=car)
        car_like.delete()
        return Response({"success": True, "message": "dislike"})


class MeLikedCarGet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetCarsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user_liked_ids = Like.objects.filter(author=self.request.user).values_list(
            "car_id", flat=True
        )
        return Car.objects.filter(id__in=user_liked_ids).order_by("-likes__created_time")

# /////////////////////////////////////////////////////////
# ////////////       GET All MARKAS       /////////////////
# /////////////////////////////////////////////////////////
class GetAllMarkasView(ListAPIView):
    queryset = Marka.objects.all()
    permission_classes = [AllowAny]
    serializer_class = GetAllMarkasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GetMarkasWithModelsFilter


# /////////////////////////////////////////////////////////
# ////////////       GET All MODELS       /////////////////
# /////////////////////////////////////////////////////////
class getAllModelsView(ListAPIView):
    queryset = CarModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = getAllModelsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GetModelsWithAvtoTypeFilter
