from .models import User

# MODELS
from .models import Auth_STATUS

# DJANGO
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError as DjangoValidationError,
)
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import update_last_login

# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

# Simple JWT
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken , RefreshToken

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
        try:
            if login_type == "username":
                current_user = User.objects.get(username=user_input)
            elif login_type == "email":
                current_user = User.objects.get(email__iexact=user_input)
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
                current_user = User.objects.get(email__iexact=user_input)
                user_email = current_user
        except ObjectDoesNotExist:
            raise ValidationError({"user": "User not found"})

        current_user.create_confirmation()

        verify_code = current_user.verify.filter(
            expire_time__gte=timezone.now(), is_confirmed=False
        ).order_by("-created_time")
        # print(verify_code)
        if verify_code.count() > 1:
            verify_code.first().delete()
            raise ValidationError(
                {"code": "You already have a valid code. Please wait until it expires."}
            )

        if not verify_code.exists():
            raise ValidationError({"code": "Code not found"})

        send_email(user_email, verify_code.first().code)
        attrs["user"] = current_user

        return attrs


# ////////////////////////////////////////////////////////
# ////////////////    VERIFY CODE   //////////////////////
# ///////////////////////////////////////////////////////
class CodeVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, write_only=True, required=True)


# ////////////////////////////////////////////////////////
# ////////////////    NEW PASSWORD    ////////////////////
# ///////////////////////////////////////////////////////
class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]

        if len(password) < 8 or len(password) > 32:
            raise ValidationError(
                {"password": "Password length must be between 8 and 32 characters."}
            )

        if password != confirm_password:
            raise ValidationError({"password": "Passwords do not match."})

        self.check_password(password)

        return attrs

    @staticmethod
    def check_password(password):
        try:
            validate_password(password)
        except Exception as e:
            raise ValidationError({"password": f"Password is not valid: {e}"})

    def update(self, instance, validated_data):
        if validated_data.get("password"):
            instance.set_password(validated_data.get("password"))

        if instance.auth_status == Auth_STATUS.EDIT_PASSWORD:
            instance.auth_status = Auth_STATUS.REGISTER

        instance.save()
        return instance


# ////////////////////////////////////////////////////////
# //////////////////   EMIAL EDIT    /////////////////////
# ////////////////////////////////////////////////////////
class EmailEditSerializer(serializers.Serializer):

    old_email = serializers.EmailField(required=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    
    def validate(self, data):
        old_emial = data.get("old_email")

        if old_emial and check_login_type(old_emial) == "email":

            user = User.objects.filter(email=old_emial).order_by("-created_time")

            if not user.exists():
                raise ValidationError({"email": "user not found"})

            user.first().create_confirmation()

            code_verify = user.first().verify.filter(
                expire_time__gte=timezone.now(), is_confirmed=False
            )
            if code_verify.count() > 1:
                code_verify.last().delete()
            send_email(old_emial, code_verify.last().code)

        return data


# ////////////////////////////////////////////////////////
# //////////////////   EMIAL VERIFY    ///////////////////
# ////////////////////////////////////////////////////////
class EmailVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, required=True)


# ////////////////////////////////////////////////////////
# ////////////////   UPDATE USER    /////////////////////
# ////////////////////////////////////////////////////////
class UpdateUserSerializer(serializers.Serializer):
    photo = serializers.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "jpg", "png", "heic", "hief"]
            )
        ],
    )
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate(self, data):
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        for input in [username, first_name, last_name]:
            self.check_input_len(input)

        return data

    @staticmethod
    def check_input_len(value):
        if value is None:
            return None
        if 5 > len(value) or len(value) > 32:
            raise ValidationError(
                {"value": f"{value} must be between 5 and 32 characters."}
            )
            
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["message"] = "Successfully changed."
        request = self.context.get('request')
        if request and instance.photo :
            data['photo'] = request.build_absolute_uri(instance.photo)
        return data

    def update(self, instance, validated_data):

        photo = validated_data.get("photo", instance.photo)

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.photo = photo

        instance.save()
        
        return instance


# ////////////////////////////////////////////////////////
# ////////////////   UPDATE PASSWORD  ////////////////////
# ////////////////////////////////////////////////////////
class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise ValidationError({"confirm_password": "Passwords do not match"})

        try:
            validate_password(new_password)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        new_password = validated_data.get("new_password")

        if not instance.check_password(password):
            raise ValidationError({"password": "Current password is incorrect"})

        instance.set_password(new_password)

        instance.save()

        return instance


# ////////////////////////////////////////////////////////
# ////////////////   GET USER         ////////////////////
# ////////////////////////////////////////////////////////
class GetUserSerializer(serializers.ModelSerializer):
    
    photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name" , 'photo']
        
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_admin'] = instance.is_staff
        return data    

    def get_photo(self , obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if obj.photo  and hasattr(obj.photo , 'url'):
                return request.build_absolute_uri(obj.photo.url)
            return None
        return obj.photo.url
        
# ////////////////////////////////////////////////////////
# ////////////  REFRESH TOKEN         ////////////////////
# ////////////////////////////////////////////////////////
class LoginRefreshSerializer(TokenRefreshSerializer):
    
    def validate(self, attrs):
        data =  super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id= access_token_instance['user_id']
        user  = get_object_or_404(User ,  id=user_id)
        update_last_login(None , user)
        data['refresh'] = attrs['refresh']
        
        return data