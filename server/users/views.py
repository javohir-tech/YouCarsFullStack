from django.shortcuts import render
from django.utils import timezone

# ////////// REST FREMEWORK ////////
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

# /////////// models ////////////
from .models import User
from .models import Auth_STATUS

# serializers
from .serializers import (
    SingUpSarializer,
    LoginSerilazer,
    LogOutSerializer,
    ForgetPasswordSerializer,
    CodeVerifySerializer,
    NewPasswordSerializer,
)

# SIMPLE JWT
from rest_framework_simplejwt.tokens import RefreshToken

# VERIFY TOKEN
from .tokens import VerifyToken

# Authentications
from .authentication import VerifyTokenAuthentication

# permissions
from .permissions import (
    IsVerifyPermission,
    CodeVerifyPermission,
    EditPasswordPermission,
)


# ////////////////////////////////////////////////////////
# /////////////////     SingUP      //////////////////////
# ////////////////////////////////////////////////////////
class SingUpView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SingUpSarializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.auth_status = Auth_STATUS.DONE
            user.save()
            token = user.token()
            return Response(
                {
                    "success": True,
                    "message": "User successfully singup",
                    "data": {
                        "username": user.username,
                        "email": user.email,
                        "tokens": {
                            "access_token": token.get("access_token"),
                            "refresh_token": token.get("refresh"),
                        },
                    },
                }
            )


# ////////////////////////////////////////////////////////
# /////////////////     LOGIN      ///////////////////////
# ////////////////////////////////////////////////////////


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerilazer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            user.auth_status = Auth_STATUS.DONE
            user.save()
            token = user.token()

            return Response(
                {
                    "success": True,
                    "message": "You have successfully logged in",
                    "data": {
                        "username": user.username,
                        "email": user.email,
                        "tokens": {
                            "access_token": token["access_token"],
                            "refresh_token": token["refresh"],
                        },
                    },
                }
            )


# ////////////////////////////////////////////////////////
# /////////////////     LOGOUT      //////////////////////
# ////////////////////////////////////////////////////////
class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogOutSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            refresh = serializer.validated_data["refresh"]
            token = RefreshToken(refresh)
            token.blacklist()
            user = self.request.user
            user.auth_status = Auth_STATUS.REGISTER
            user.save()
            return Response({"success": True, "message": "You are success logout"})


# ////////////////////////////////////////////////////////
# //////////////    FORGET PASSWORD   ///////////////////
# ///////////////////////////////////////////////////////
class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            user.auth_status = Auth_STATUS.VERIFY_CODE
            user.save()
            token = VerifyToken.for_user(user)
            return Response(
                {
                    "success": True,
                    "message": "We’ve sent a message to your email. Please check your inbox.",
                    "data": {
                        "email": user.email,
                        "username": user.username,
                        "tokens": {
                            "verify_token": str(token),
                        },
                    },
                }
            )


# ////////////////////////////////////////////////////////
# ////////////////    VERIFY CODE   //////////////////////
# ///////////////////////////////////////////////////////
class CodeVerifyView(APIView):
    permission_classes = [IsVerifyPermission, CodeVerifyPermission]
    authentication_classes = [VerifyTokenAuthentication]

    def post(self, request):
        serializer = CodeVerifySerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            code = data["code"]
            user = request.user
            current_code = user.verify.filter(
                expire_time__gte=timezone.now(), code=code, is_confirmed=False
            )

            if current_code.exists():
                current_code.first().is_confirmed = True
                user.auth_status = Auth_STATUS.EDIT_PASSWORD
                current_code.first().save()
                user.save()
                token = VerifyToken.for_user(user)
                return Response(
                    {
                        "success": True,
                        "message": "Code has been verified successfully.",
                        "auth_status": user.auth_status,
                        "data": {"tokens": {"code_edit_token": str(token)}},
                    }
                )
            raise ValidationError({"code": "Invalid verification code."})


# ////////////////////////////////////////////////////////
# ////////////////    NEW PASSWORD    ////////////////////
# ///////////////////////////////////////////////////////
class NewPasswordView(APIView):
    permission_classes = [IsVerifyPermission, EditPasswordPermission]
    authentication_classes = [VerifyTokenAuthentication]

    def put(self, request):

        serializer = NewPasswordSerializer(
            instance=self.request.user, data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            
            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "parol o'zgartrildi , login qilshingizni soraymiz",
                }
            )
