from rest_framework import serializers
from . models import Product, Category, Reviews, ProductImage
from django.contrib.auth import get_user_model
from PIL import Image

Users = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users.objects.create(**validated_data)
        user.set_password(password)  # set password for user
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'Name', 'Description']


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['id', 'Product', 'Image']


class ProductSerilizer(serializers.ModelSerializer):
    Category = CategorySerializer
    Images = ProductImageSerializer(many=True, read_only=True)

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
            raise serializers.ValidationError({'Stock Quantity cannot be nagative'})
        return value

    def validate_Image(self, value):
        img = Image.open(value)
        if img.format.lower() != 'jpeg':
            raise serializers.ValidationError({'Error': 'Only JPEG format is allowed'})
        return value

    def validate_Image_size(self, value):
        max_size_bytes = 5242880
        if value > max_size_bytes:
            raise serializers.ValidationError({'Error': f'Image size exceeds {max_size_bytes} MB'})
        return value


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ['id', 'User', 'Product', 'Comment', 'Ratings', 'Created_at']
