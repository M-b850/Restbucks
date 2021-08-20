from rest_framework import serializers
from core.models import *

class ProductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Production
        fields = ('id', 'name', 'price')


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ('id', 'product', 'quantity')
        read_only_fields = ('id', 'status', 'price',)


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('name',)
        read_only_fields = ('id',)


class OrderTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('tag',)
        read_only_fields = ('id',)
