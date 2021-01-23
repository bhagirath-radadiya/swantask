from django.urls import path
from . import views

urlpatterns = [
    path('viewProfile/', views.viewProfile, name='viewProfile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),

]
