from rest_framework.pagination import PageNumberPagination

class DefaulPaginationNumber(PageNumberPagination):
    page_size = 10