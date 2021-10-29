from django.urls import path
from . import views
from django.views.generic.edit import CreateView, UpdateView

urlpatterns = [
   # path('hello/', hello.views.index, name='hello'),
    path('msgserver/get/<slug:key>/', views.getmessage, name='key'),
    path('msgserver/create/', views.Createmessage.as_view(), name='create'),
    path('msgserver/update/<slug:key>/', views.UpdateMessage.as_view(), name='update'),
    path('msgserver/', views.returnall, name='returnall'),
]