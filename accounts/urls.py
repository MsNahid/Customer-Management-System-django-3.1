from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.home, name="home"),
    path("products/", views.products, name="products"),
    path("customer/<str:request_id>/", views.customer, name="customer"),
]

