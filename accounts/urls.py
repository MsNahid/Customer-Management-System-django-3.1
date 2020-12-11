from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.home, name="home"),
    path("products/", views.products, name="products"),
    path("customer/<str:request_id>/", views.customer, name="customer"),
    path('create_order/<str:request_id>/', views.createOrder, name="createOrder"),
    path('update_order/<str:request_id>/', views.updateOrder, name="updateOrder"),
    path('delete_order/<str:request_id>/', views.deleteOrder, name="deleteOrder"),

]

