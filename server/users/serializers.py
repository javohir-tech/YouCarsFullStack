from .models import User

# DJANGO
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Simple JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):

        current_email = attrs.get("email")
        password = attrs.get("password")

        if 8 > len(password) or len(password) > 32:
            raise ValidationError(
                {"password": "The password length must be between 8 and 32 characters."}
            )

        try:
            current_user = User.objects.get(email=current_email)
        except ObjectDoesNotExist:
            raise ValidationError({"user": "User not found"})

        user = authenticate(username=current_user.username, password=password)

        if not user:
            raise ValidationError({"user": "Email or password is incorrect"})

        attrs["user"] = current_user

        return attrs
    
# ////////////////////////////////////////////////////////
# /////////////////     LOGOUT      //////////////////////
# ////////////////////////////////////////////////////////
class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required = True)

