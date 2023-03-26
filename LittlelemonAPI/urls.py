from django.urls import path
from . import views

urlpatterns = [
     path('menuitem', views.MenuItemView.as_view()),
     path('category', views.CategoryView.as_view()),
     path('menuitem/<int:pk>', views.single_item),
     path('cart', views.CartView.as_view()),
     path('orders', views.OrderView.as_view()),
     path('orderitem', views.OrderItemView.as_view()),
]