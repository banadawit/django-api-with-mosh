from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection, Review

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','description','slug','inventory', 'unit_price', 'price_with_tax', 'collection']  
   
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')  
 
    def get_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.2)
    
class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']  # Add product_count
    product_count = serializers.IntegerField(read_only=True)  # Add product_count field

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'product' , 'date']
