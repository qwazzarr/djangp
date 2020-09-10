from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.conf.urls import include

app_name = 'kchat'
urlpatterns = [
    path('talk/', views.TalkMain.as_view() , name = 'talk'),
    path('messages/', views.TalkMessages.as_view(), name = 'messages'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('user/<int:pk>', views.PrivateTalk.as_view(), name = 'privatetalk'),
    path('user/<int:pk>/message' , views.PrivateMessages.as_view(), name = 'privatemessage'),
]
