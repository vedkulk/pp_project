from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('product/<int:pk>', views.product, name="product"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name="login"),
    path('login/Registration.html', views.Registration, name="Registration"),
    path('update_item/', views.updateItem, name='update_item')
]
