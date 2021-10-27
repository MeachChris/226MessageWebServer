from django.urls import path
from . import views

urlpatterns = [
    path('get/<slug:key>/', views.getmessage, name='key')
]