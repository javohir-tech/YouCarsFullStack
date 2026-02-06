from django.shortcuts import render
from django.utils import timezone

# ////////// REST FREMEWORK ////////
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
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
    LoginRefreshSerializer,
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
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "confirm_password": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["email", "username", "password", "confirm_password"],
        ),
        responses={
            200: openapi.Response("User created successfully"),
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User Sing In with email or username",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_input": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["user_input", "password"],
        ),
        responses={
            200: openapi.Response("User login successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User Logout",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["refresh"],
        ),
        responses={
            200: openapi.Response("User logout successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="get verify code with email or username",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_input": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["user_input"],
        ),
        responses={
            200: openapi.Response("User verify code send successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="check verify code",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "code": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=["code"],
        ),
        responses={
            200: openapi.Response("checked code successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User set new password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "confirm_password": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["password", "confirm_password"],
        ),
        responses={
            200: openapi.Response("User change new passwordd successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User change email address",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "old_email": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["email", "old_email"],
        ),
        responses={
            200: openapi.Response("User send code successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User check verify code",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"code": openapi.Schema(type=openapi.TYPE_NUMBER)},
            required=["code"],
        ),
        responses={
            200: openapi.Response("checked verify code successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User update",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "photo": openapi.Schema(type=openapi.TYPE_FILE),
            },
            required=["first_name", "username", "last_name", "photo"],
        ),
        responses={
            201: openapi.Response("User update successfully"),
            400: openapi.Response("Bad request"),
        },
    )
    def put(self, request):

        serializer = UpdateUserSerializer(
            instance=self.request.user, data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User update patch",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "photo": openapi.Schema(type=openapi.TYPE_FILE),
            },
            required=[],
        ),
        responses={
            201: openapi.Response("User update successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="User update password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "new_password": openapi.Schema(type=openapi.TYPE_STRING),
                "confirm_password": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["password", "new_password", "confirm_password"],
        ),
        responses={
            201: openapi.Response("User update password successfully"),
            400: openapi.Response("Bad request"),
        },
    )
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

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="get User",
        responses={
            200: openapi.Response("User get successfully"),
            400: openapi.Response("Bad request"),
        },
    )
    def get(self, request):
        serializer = GetUserSerializer(
            instance=request.user, context={"request": request}
        )
        return Response(serializer.data)


# ////////////////////////////////////////////////////////
# ////////////  REFRESH TOKEN         ////////////////////
# ////////////////////////////////////////////////////////
class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer
    
    
# ////////////////////////////////////////////////////////
# ////////////  DELETE USER IMAGE     ////////////////////
# ////////////////////////////////////////////////////////
class UserImageDelete(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.photo :
            user.photo.delete(save=True)
            return Response({
                "success":  True, 
                "message": "rasm ochirildi"
            } , status=status.HTTP_200_OK)    
        else :
            return Response({
                "message" : "rasmni ozi yoqku uka"
            })