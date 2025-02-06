from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','description','slug','inventory', 'unit_price', 'price_with_tax', 'collection']  
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')  
    # collection = serializers.HyperlinkedRelatedField(
    #     view_name='collection-detail',  # URL pattern name
    #     queryset=Collection.objects.all()
    # )
    
    # collection = CollectionSerializer() # this is used to get title and id of collection

    # collection = serializers.StringRelatedField()  # this is also used to get title of collection
    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())  # this is used to get id of collection
    
    def get_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.2)
    
    # below code is used to create and update product       
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product    
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.save()
    #     return instance

class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']  # Add product_count
    product_count = serializers.IntegerField()