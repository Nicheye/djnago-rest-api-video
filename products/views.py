from django.shortcuts import render
from . models import Product,User
# Create your views here.
from random import choice
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_202_ACCEPTED,HTTP_204_NO_CONTENT
from . serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from .producer import publish
class ProductViewSet(viewsets.ViewSet):
    def list(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        
        return Response(serializer.data)

    def create(self,request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created',serializer.data)
        return Response(serializer.data,status=HTTP_201_CREATED)
    def retrieve(self,request,pk=None):
        product =Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def update(self,request,pk=None):
        product =Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated',serializer.data)
        return Response(serializer.data,status=HTTP_202_ACCEPTED)

    
    def destroy(self,request,pk=None):
        product =Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted',pk)
        return Response(status=HTTP_204_NO_CONTENT)
class UserApiView(APIView):
    def get(self,_):
        users = User.objects.all()
        user = choice(users)
        return Response({
            'id': user.id
        })