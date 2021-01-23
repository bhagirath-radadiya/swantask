from django.urls import path
from . import views

urlpatterns = [
    path("loadPayment/", views.loadPayment, name="loadPayment"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
]
