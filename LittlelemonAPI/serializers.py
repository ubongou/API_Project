from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title','price','featured','category']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['title','price','featured','category']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['title','price','featured','category']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['title','price','featured','category']

    