from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView   
from rest_framework import status
from .models import Product, Collection
from django.db.models import Count
from .serializers import ProductSerializer, CollectionSerializer

class ProductList(ListCreateAPIView):
    queryset =  Product.objects.select_related('collection').all() 
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

# class ProductList(APIView):

#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'id'
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.order_items.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_409_CONFLICT)                                                                               
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CollectionDetail(RetrieveUpdateDestroyAPIView):   
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it contains products.'},
                            status=status.HTTP_409_CONFLICT)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)