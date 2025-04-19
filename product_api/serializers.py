from rest_framework import serializers
from . models import Product
from django.contrib.auth import get_user_model

Users = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = Users.objects.create(**validated_data)
        user.password = password
        user.save()
        return user


class ProductSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate_Price(self, value):
        if value <= 0:
            return serializers.ValidationError({'Error': 'Price cannot be 0'})
        return value

    def validate_Name(self, value):
        if not value.strip():
            return serializers.ValidationError({'Error': 'Name cannot be Blank'})
        return value

    def validate_Stock_Quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(['Stock Quantity cannot be nagative'])
        return value
