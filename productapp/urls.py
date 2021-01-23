from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('viewProductDetail/', views.viewProductDetail, name='viewProductDetail'),

    path('shop/', views.shop, name='shop'),


]
