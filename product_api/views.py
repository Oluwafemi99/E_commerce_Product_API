from django.shortcuts import render
from .models import Users, Product, Category
from .serializers import UserSerializer, ProductSerilizer, CategorySerializer
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import ProductPagination, CategoryPagination
from django.core.exceptions import PermissionDenied


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
            raise PermissionDenied({'You are not Authorised'})
        serializer.save(User=self.request.user)


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
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def perform_update(self, serializer):
        product = self.get_object()
        if product.User != self.request.user:
            raise PermissionDenied({'you are not authorised'})
        serializer.save(User=self.request.user)


class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductSerilizer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def perform_destroy(self, instance):
        if instance.User != self.request.user:
            raise PermissionDenied({'You are not Authorised'})
        instance.delete()


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['Name', 'Description']
    filterset_fields = ['Name']
    pagination_class = CategoryPagination
