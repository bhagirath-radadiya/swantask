from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('insertLogin/', views.insertLogin, name='insertLogin'),

    path('registration/', views.registration, name='registration'),
    path('insertRegistration/', views.insertRegistration, name='insertRegistration'),

    path('logout/', views.logout, name='logout'),

]
