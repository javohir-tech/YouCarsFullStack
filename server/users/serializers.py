from .models import User

# DJANGO
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Simple JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# shared
from shared.utils import check_login_type, send_email

# ////////////////////////////////////////////////////////
# /////////////////     SINGUP      //////////////////////
# ////////////////////////////////////////////////////////


class SingUpSarializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "confirm_password"]
        read_only_fields = ["id"]
        extra_kwargs = {"confirm_password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise ValidationError({"password": "Passwords do not match."})

        if 8 > len(password) or len(password) > 32:
            raise ValidationError(
                {"password": "The password length must be between 8 and 32 characters."}
            )

        return attrs

    def validate_username(self, value):
        if value.isdigit():
            raise ValidationError("The username must consist of letters.")

        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


# ////////////////////////////////////////////////////////
# /////////////////     LOGIN      ///////////////////////
# ////////////////////////////////////////////////////////


class LoginSerilazer(serializers.Serializer):
    user_input = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):

        user_input = attrs.get("user_input")
        password = attrs.get("password")

        if 8 > len(password) or len(password) > 32:
            raise ValidationError(
                {"password": "The password length must be between 8 and 32 characters."}
            )
        login_type = check_login_type(user_input)
        print("=" * 50)
        print(login_type)
        print("=" * 50)
        try:
            if login_type == "username":
                current_user = User.objects.get(username=user_input)
            elif login_type == "email":
                current_user = User.objects.get(email=user_input)
        except ObjectDoesNotExist:
            raise ValidationError({"user": "User not found"})

        user = authenticate(username=current_user.username, password=password)

        if not user:
            raise ValidationError({"user": "Email , username or password is incorrect"})

        attrs["user"] = current_user

        return attrs


# ////////////////////////////////////////////////////////
# /////////////////     LOGOUT      //////////////////////
# ////////////////////////////////////////////////////////
class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


# ////////////////////////////////////////////////////////
# //////////////    FORGET PASSWORD   ///////////////////
# ///////////////////////////////////////////////////////
class ForgetPasswordSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user_input = attrs.get("user_input")

        auth_type = check_login_type(user_input)

        try:
            if auth_type == "username":
                current_user = User.objects.get(username=user_input)
                user_email = current_user.email
            elif auth_type == "email":
                current_user = User.objects.get(email=user_input)
                user_email = current_user
        except ObjectDoesNotExist:
            raise ValidationError({"user": "user topilmadi "})

        current_user.create_confirmation()

        verify_code = current_user.verify.filter(
            expire_time__gte=timezone.now(), is_confirmed=False
        ).order_by('-created_time')
        print(verify_code)
        if verify_code.count() > 1:
            verify_code.first().delete()
            raise ValidationError(
                {"code": "sizda yaroqli kod bor tugash vaqtini kuting"}
            )

        if not verify_code.exists():
            raise ValidationError({"code": "Kod topilmadi"})

        send_email(user_email, verify_code.first().code)

        return attrs


# class
