from django.urls import path
from . import views

urlpatterns = [
     # path('menu-item', views.MenuItemView.as_view()),
     path('categories', views.CategoryView.as_view()),
     # path('menu-item/<str:title>', views.single_item),
     path('cart/menu-items', views.CartView.as_view()),
     # path('menu-item', views.MenuItemView.as_view()),
     path('orders', views.OrdersView.as_view()),
     path('orders/<int:pk>', views.OrderDetailView.as_view()),
     path('orderitem', views.OrderItemView.as_view()),
     path('groups/manager/users',views.manager),
     path('groups/delivery-crew/users',views.delivery_crew),
     path('users/me', views.me),
     path('menu-items/', views.MenuItemList.as_view()),
     path('menu-items/<int:pk>', views.MenuItemDetail.as_view()),
]