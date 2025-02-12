from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .filters import ProductFilter
from.pagination import DefaulPaginationNumber
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
 

# To find product by title or description we use Serching
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination # To do pagination for each class
    pagination_class = DefaulPaginationNumber
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        # if product.order_items.count() > 0:
        #     return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_409_CONFLICT)                                                                               
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_409_CONFLICT)
        return super().destroy(request, *args, **kwargs)    

# below code will do the same as above code but in a different way by using APIView
# class ProductList(ListCreateAPIView):
#     queryset =  Product.objects.all() 
#     serializer_class = ProductSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'id'
    
#     def delete(self, request, pk):
#             product = get_object_or_404(Product, pk=pk)
#             if product.order_items.count() > 0:
#                 return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_409_CONFLICT)                                                                               
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        # if collection.products.count() > 0:
        #     return Response({'error': 'Collection cannot be deleted because it contains products.'},
        #                     status=status.HTTP_409_CONFLICT)
        if OrderItem.objects.filter(
            product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'},
                  status=status.HTTP_409_CONFLICT)
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # This method filters reviews based on the product ID provided in the URL.
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk']).select_related('product')

    def get_serializer_context(self):
        return {'request': self.request}