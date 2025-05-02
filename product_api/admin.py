from django.contrib import admin
from .models import Users, Product, Category, Reviews, ProductImage


# Register your models here.
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Description', 'Price', 'Category', 'Stock_Quantity', 'Image_Url', 'Created_at', 'User']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Description']


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'User', 'Product', 'Comment', 'Ratings', 'Created_at']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'Product', 'Image']
