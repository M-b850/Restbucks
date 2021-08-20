from django.shortcuts import redirect

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from client.permissions import IsOwner
from rest_framework.response import Response

from core.models import Customization, Production, Order, Tag
from client.serializers import (
    ProductionSerializer, OrderSerializer, TagSerializer, OrderTagSerializer, BaseOrderSerializer
)

class ProductionList(generics.GenericAPIView):
    """ List of all productions. """
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer

    def get(self, request, format=None):
        """ Return a list of all productions. """
        productions = Production.objects.all()
        serializer = ProductionSerializer(productions, many=True)
        return Response(serializer.data)


class OrderCreate(generics.CreateAPIView):
    """ Create an order. """
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )
    
    def create(self, request, *args, **kwargs):
        """ Redirect to the order detail after creating an order. """
        response = super().create(request, *args, **kwargs)
        production = Production.objects.get(pk=request.data['product'])
        customization = production.customization_set.all()

        if len(customization) == 0:
            return redirect('/client/')
        
        return redirect('/client/order/customization/' + str(response.data['id']))

    def perform_create(self, serializer):
        """ Save the post data when creating a new order. """
        serializer.save(owner=self.request.user)


class OrderCustomizations(APIView):
    """ List of all Tags for a given order. """
    serializer_class = OrderTagSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        order = Order.objects.get(id=self.kwargs['pk'])
        production = Production.objects.get(id=order.product.pk)
        customization = production.customization_set.all().first()
        tags = customization.tag_set.all()
        return tags

    def get(self, request, *args, **kwargs):
        """ Return a list of all available tags for given order. """
        tags = self.get_queryset()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        """ add a tag for given order. """
        obj = Order.objects.get(id=self.kwargs['pk'])
        # If tag exists, return 400
        if obj.tag is not None:
            return Response({'error': 'You\'ve Choosen one already!'}, status=status.HTTP_400_BAD_REQUEST)
        # If doesn't exist, save orders tag
        obj.tag = Tag.objects.get(pk=request.data['tag'])
        obj.customization = Customization.objects.get(pk=obj.tag.customization.pk)
        obj.save()
        return Response({'success': 'Tag saved.'}, status=status.HTTP_200_OK)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete an order. """
    queryset = Order.objects.all()
    serializer_class = BaseOrderSerializer
    permission_classes = (IsOwner,)

    def get_object(self):
        """ Return the order. """
        return Order.objects.get(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        """ Return the order. """
        order = self.get_object()
        serializer = BaseOrderSerializer(order)
        return Response(serializer.data)

    
    def put(self, request, *args, **kwargs):
        """ Update the order. """

        order = self.get_object()

        # if status not waiting, return 400
        if not order.status == 'waiting':
            return Response({'error': 'You\re out of time, sorry :).'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BaseOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """ Delete the order. """
        order = self.get_object()
        # if status not waiting, return 400
        if not order.status == 'waiting':
            return Response({'error': 'You\re out of time, sorry :).'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.delete()
        return Response(message='Order deleted.', status=status.HTTP_204_NO_CONTENT)