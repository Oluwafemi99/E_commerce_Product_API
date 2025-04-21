from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):

    def __str__(self):
        return self.username


class Category(models.Model):
    Name = models.CharField(max_length=20)
    Description = models.CharField(max_length=200)

    def __str__(self):
        return self.Name


class Product(models.Model):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200,)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Products')
    Stock_Quantity = models.IntegerField()
    Image_Url = models.URLField()
    Created_at = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
