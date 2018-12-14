from django.db.models import Q
from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from rest_framework.serializers import CharField, IntegerField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class MobileNumberSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = MobileNumber
        fields = ["user", "mobile_number"]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.set_password(user_data['password'])
        user.save()
        mobile_number = MobileNumber.objects.update_or_create(user=user,
                                                              mobile_number=validated_data.pop("mobile_number"))
        return mobile_number


class UserLoginSerializer(serializers.ModelSerializer):
    username = CharField()
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "token"]

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data['username']
        password = data['password']
        if not username:
            raise ValidationError("A username is required to login")
        user = User.objects.filter(Q(username=username)).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Username or password is incorrect")
        return data


class ConcertsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concerts
        fields = ["date", "location", "band", "price", "seats_left"]


class AuthorizationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorizationCode
        fields = '__all__'
