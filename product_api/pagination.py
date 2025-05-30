from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class CategoryPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page size'
    max_page_size = 100


class ReviewsPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page size'
