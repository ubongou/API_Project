from rest_framework import generics, permissions
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from django.forms.models import model_to_dict

# Create your views here.

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view()
def single_item(request,title):
    item=get_object_or_404(MenuItem,title=title)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view()
def single_item2(request,id):
    item=get_object_or_404(Order,pk=id)
    serialized_item = OrderSerializer(item)
    return Response(serialized_item.data)


class MenuItemList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    # def get_queryset(self):
    #     return MenuItem.objects.all()
    
    # def post(self, request, *args, **kwargs):
    #     if self.request.user.is_superuser:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST)


class MenuItemDetail(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.all()
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST)        
    
class OrderItemView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def manager(request):
    if request.method=='GET':
        managers = Group.objects.get(name='Manager')
        usernames = list(managers.user_set.values_list('username', flat=True))
        return Response(usernames)
    username = request.data['username']
    if username:
        user = get_object_or_404(User,username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response ({'message':'ok'})
    return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def delivery_crew(request):
    if request.method=='GET':
        delivery_crew = Group.objects.get(name='Delivery-Crew')
        usernames = list(delivery_crew.user_set.values_list('username', flat=True))
        return Response(usernames)
    username = request.data['username']
    if username:
        user = get_object_or_404(User,username=username)
        delivery_crew = Group.objects.get(name='Delivery-Crew')
        if request.method == 'POST':
            delivery_crew.user_set.add(user)
        elif request.method == 'DELETE':
            delivery_crew.user_set.remove(user)
        return Response ({'message':'ok'})
    return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST)


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            # if user is a manager, return all orders
            return Order.objects.all()
        elif self.request.user.is_staff:
            # if user is a delivery crew, return orders assigned to the delivery crew
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            # if user is a customer, return orders created by the user
            try:
                Order.objects.filter(user=self.request.user)
            except:
                return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST)
            return Order.objects.filter(user=self.request.user)
    def post(self, request, *args, **kwargs):
        # get cart items for the user
        cart_items = Cart.objects.filter(user=request.user)

        # create new order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)
        total=0

        # create order items from cart items
        for cart_item in cart_items:
            total+=cart_item.price
            OrderItem.objects.create(order=order, menuitem=cart_item.menuitem, quantity=cart_item.quantity, unit_price=cart_item.unit_price, price = cart_item.price)

        
        order = serializer.save(total=total)
        # delete cart items for the user
        cart_items.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderItemView(generics.RetrieveAPIView, generics.DestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            # if user is a manager, return all order items
            return OrderItem.objects.all()
        elif self.request.user.is_staff:
            # if user is a delivery crew, return orders assigned to the delivery crew
            return OrderItem.objects.filter(delivery_crew=self.request.user)
        else:
            # if user is a customer or delivery crew, return order items for orders created by the user
            return OrderItem.objects.filter(user=self.request.user)
        
 
    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = self.get_queryset()
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class OrderDetailView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()
    
    def put(self, request, *args, **kwargs):
        if notrequest.user.is_staff:
            return Response({'detail': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'error'}, status.HTTP_400_BAD_REQUEST) 
# class OrderDetailAPIView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def get(self, request, id, format=None):
#         order = get_object_or_404(Order.objects.filter(user=request.user), id=id)
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)
    
#     def put(self, request, id, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#     # def put(self, request, id, format=None):
#     #     order = get_object_or_404(Order.objects.all(), id=id)
#     #     serializer = OrderSerializer(order, data=request.data)
#     #     if serializer.is_valid() and self.request.user.is_superuser:
#     #         serializer.save()
#     #         return Response(serializer.data)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # def patch(self, request, id, format=None):
#     #     order = get_object_or_404(Order.objects.all(), id=id)
#     #     if request.user.is_superuser:
#     #         order.delivery_crew = request.user.delivery_crew
#     #     elif request.user.is_staff:
#     #         order.status = request.data['status'] 
#     #     else:
#     #         return Response({'detail': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
#     #     order.save()
#     #     serializer = OrderSerializer(order)
#     #     return Response(serializer.data)

#     def delete(self, request, id, format=None):
#         if self.request.user.is_superuser:
#             order = get_object_or_404(Order.objects.all(), id=id)
#             order.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)