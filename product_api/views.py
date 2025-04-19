from django.shortcuts import render
from .models import Users, Product
from .serializers import UserSerializer, ProductSerilizer
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import ProductPagination
from django.db.models import Q


# Create your views here.
class UserCreateView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Users.objects.filter(pk=self.request.user.pk)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Users.objects.all()


class productCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        User = serializer.validated_data['User']
        if User != self.request.user:
            return PermissionError({'You are not Authorised'})
        serializer.save(user=self.request.user)


class ProductDetailsView(generics.RetrieveAPIView):
    serializer_class = ProductSerilizer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerilizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()

        # Apply optional filters
        category = self.request.query_params.get('Category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        stock = self.request.query_params.get('in_stock', None)

        if category:
            queryset = queryset.filter(category__iexact=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if stock is not None:
            # Filter products with positive stock quantity
            queryset = queryset.filter(stock_quantity__gt=0) if stock.lower() == "true" else queryset.filter(stock_quantity__lte=0)

        return queryset


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerilizer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['Name', 'Category']
    pagination_class = ProductPagination


class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerilizer
    permission_classes =[permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter()