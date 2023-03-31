from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=MenuItem
        fields =['title','price','featured','category']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user','menuitem','quantity','unit_price','price'] 
        read_only_fields = ['user','unit_price','price']

       

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user','delivery_crew','status','total','date']
        read_only_fields = ['user','total','date']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    