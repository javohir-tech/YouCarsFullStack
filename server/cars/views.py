from django.shortcuts import render

# //////////////// REST FRAMEWORK ////////////////
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

# ///////////////////// MODELS //////////////////////////
from .models import AvtoMobileType

# //////////// SERIALIZERS  /////////////////////////////
from .serializers import (
    GetAvtoTypeSerializer,
    GetMarkaWithTypeSerializer,
    AvtoTypeMarkaSerializer,
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
