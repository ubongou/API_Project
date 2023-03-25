from django.urls import path
from . import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('books/<int:pk>', views.SingleBookView.as_view()),
]