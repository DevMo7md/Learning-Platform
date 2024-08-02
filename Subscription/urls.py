from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe-success/', views.subscribe_success, name='subscribe_success'),
]
