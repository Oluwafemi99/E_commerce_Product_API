from django.urls import path, include
from . views import (UserCreateView, UserDetailsView, UserListView,
                     productCreateView, ProductDetailsView, ProductListView,
                     ProductDeleteView, ProductUpdateView, ProductSearchView,
                     CategoryView, ReviewsCreateView, ReviewsListViews,
                     productImageUploadView)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'categories', CategoryView, basename='category')


urlpatterns = [
    path('user/create/', UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/detail/', UserDetailsView.as_view(), name='user_detail'),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('product/create/', productCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/detail/', ProductDetailsView.as_view(), name='product_detail'),
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/search/', ProductSearchView.as_view(), name='product-search'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', obtain_auth_token, name='logout'),
    path('api/', include(router.urls)),
    path('reviews/create/', ReviewsCreateView.as_view(), name='reviews_create'),
    path('reviews/list/', ReviewsListViews.as_view(), name='reviews_list'),
    path('image/upload/', productImageUploadView.as_view(), name='image_upload'),
]
