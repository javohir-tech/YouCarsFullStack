from django.shortcuts import render
from django.utils import timezone

# ////////// REST FREMEWORK ////////
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

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
    EmailEditSerializer,
    EmailVerifySerializer,
    UpdateUserSerializer,
    UpdatePasswordSerializer,
    GetUserSerializer,
    LoginRefreshSerializer
)

# SIMPLE JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

# VERIFY TOKEN
from .tokens import VerifyToken, EmailEditToken

# Authentications
from .authentication import VerifyTokenAuthentication, EmailEditAuthentication

# permissions
from .permissions import (
    IsVerifyPermission,
    CodeVerifyPermission,
    EditPasswordPermission,
    EditEmailPermissions,
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# ////////////////////////////////////////////////////////
# /////////////////     SingUP      //////////////////////
# ////////////////////////////////////////////////////////
class SingUpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["email", "password"],
        ),
        responses={
            201: openapi.Response("User created successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(tags=["auth"])
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

    @swagger_auto_schema(tags=["auth"])
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

    @swagger_auto_schema(tags=["auth"])
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

    @swagger_auto_schema(tags=["auth"])
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
                verify_obj = current_code.first()
                verify_obj.is_confirmed = True
                verify_obj.save()
                user.auth_status = Auth_STATUS.EDIT_PASSWORD

                user.save()
                token = VerifyToken.for_user(user)
                return Response(
                    {
                        "success": True,
                        "message": "Code has been verified successfully.",
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

    @swagger_auto_schema(tags=["auth"])
    def put(self, request):

        serializer = NewPasswordSerializer(
            instance=self.request.user, data=request.data
        )

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Your password has been changed successfully. Please log in",
                }
            )


# ////////////////////////////////////////////////////////
# //////////////////   EMIAL EDIT    /////////////////////
# ////////////////////////////////////////////////////////
class EditEmailView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["auth"])
    def post(self, request):
        serializer = EmailEditSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            token = EmailEditToken.for_user(
                self.request.user,
                serializer.validated_data["email"],
                serializer.validated_data["old_email"],
            )
            return Response(
                {
                    "success": True,
                    "message": "We’ve sent a message to your email. Please check your inbox",
                    "data": {"token": {"email_edit_token": str(token)}},
                }
            )


# ////////////////////////////////////////////////////////
# //////////////////   EMIAL Verify    ///////////////////
# ////////////////////////////////////////////////////////
class EmailVerifyView(APIView):
    permission_classes = [EditEmailPermissions]
    authentication_classes = [EmailEditAuthentication]

    @swagger_auto_schema(tags=["auth"])
    def post(self, request):

        serializer = EmailVerifySerializer(
            instance=self.request.user, data=request.data
        )

        if serializer.is_valid(raise_exception=True):

            new_email = request.auth.get("new_email")
            old_email = request.auth.get("old_email")
            code = serializer.validated_data.get("code")

            user = User.objects.get(email=old_email)

            if user is None:
                raise ValidationError({"email": "User not found"})

            current_user = User.objects.filter(email=new_email)
            if current_user.exists():
                raise ValidationError(
                    {"email": "This email address is already in use."}
                )

            verify_code = user.verify.filter(
                expire_time__gte=timezone.now(), code=code, is_confirmed=False
            )

            if verify_code.exists():
                verify_obj = verify_code.first()
                verify_obj.is_confirmed = True
                verify_obj.save()
                user.email = new_email
                user.save()
            else:
                raise ValidationError(
                    {"code": "The verification code is invalid or expired."}
                )

            return Response(
                {
                    "success": True,
                    "message": "Email address has been successfully updated.",
                    "data": {"email": new_email, "username": user.username},
                }
            )


# ////////////////////////////////////////////////////////
# ////////////////   UPDATE USER    /////////////////////
# ////////////////////////////////////////////////////////
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["auth"])
    def put(self, request):

        serializer = UpdateUserSerializer(instance=self.request.user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["auth"])
    def patch(self, request):
        serializer = UpdateUserSerializer(
            instance=self.request.user, data=request.data, partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# ////////////////////////////////////////////////////////
# ////////////////   UPDATE PASSWORD  ////////////////////
# ////////////////////////////////////////////////////////
class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["auth"])
    def put(self, request):

        serializer = UpdatePasswordSerializer(
            instance=self.request.user, data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            new_pass = serializer.save()
            return Response(
                {"success": True, "message": "parol muvafaqiyatli ozgartirildi"}
            )


# ////////////////////////////////////////////////////////
# ////////////////   GET USER         ////////////////////
# ////////////////////////////////////////////////////////
class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["auth"])
    def get(self, request):
        serializer = GetUserSerializer(instance=request.user)
        return Response(serializer.data)

# ////////////////////////////////////////////////////////
# ////////////  REFRESH TOKEN         ////////////////////
# ////////////////////////////////////////////////////////
class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer