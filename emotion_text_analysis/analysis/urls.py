from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process_video/', views.process_video, name='process_video'),
]