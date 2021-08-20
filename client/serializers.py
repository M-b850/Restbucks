from rest_framework import serializers
from core.models import *

class ProductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Production
        fields = ('id', 'name', 'price')


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'product', 'quantity', 'consume_location')
        read_only_fields = ('id', 'status', 'price',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class OrderTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('tag',)

    def to_representation(self, obj):
        return {
            'name': obj.name
        }


class BaseOrderSerializer(serializers.ModelSerializer):
    tag = OrderTagSerializer()
    class Meta:
        model = Order
        fields = ('id', 'product', 'quantity', 'customization', 'tag', 'status', 'price', 'consume_location')
        read_only_fields = ('id', 'status', 'price', 'customization',)

    def to_representation(self, obj):
        if obj.tag == None:
            tag_ = None
        else:
            tag_ = obj.tag.name

        return {
            'product': obj.product.name,
            'quantity': obj.quantity,
            'customization': obj.customization,
            'tag': tag_,
            'status': obj.status,
            'consume_location': obj.consume_location,
            'price': obj.price,
        }

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.customization = validated_data.get('customization', instance.customization)
        # get item of OrderedDict
        tag = list(validated_data.get('tag').values())[0]

        if not tag is None:
            instance.tag = tag

        instance.save()
        return instance