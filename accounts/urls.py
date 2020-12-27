from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user-page/', views.userPage, name="user-page"),
    path("products/", views.products, name="products"),
    path("customer/<str:request_id>/", views.customer, name="customer"),

    path('create_order/<str:request_id>/', views.createOrder, name="createOrder"),
    path('update_order/<str:request_id>/', views.updateOrder, name="updateOrder"),
    path('delete_order/<str:request_id>/', views.deleteOrder, name="deleteOrder"),

]

