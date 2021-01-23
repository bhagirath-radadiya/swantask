from django.urls import path
from . import views

urlpatterns = [
    path('addToCart/<str:foo>/', views.addToCart, name='addToCart'),
    path('cart/', views.cart, name='cart'),
    path('updateCart/', views.updateCart, name='updateCart'),
    path('deleteOrder/', views.deleteOrder, name='deleteOrder'),
    path('couponCode/', views.couponCode, name='couponCode'),

    path('checkout/', views.checkout, name='checkout'),

]
