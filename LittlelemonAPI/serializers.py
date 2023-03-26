from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    price = 5
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category']


class CartSerializer(serializers.ModelSerializer):
    # price=MenuItem
    #unitprices = MenuItemSerializer('price')
    class Meta:
        model = Cart
        fields = ['user','quantity','menuitem'] 
       

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['title','price','featured','category']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['title','price','featured','category']

    