from django.urls import path
from . import views

app_name = 'fingerprinting'

urlpatterns = [
    path('', views.index, name='index'),
    path('recognize/', views.recognize_audio, name='recognize_audio'),
    path('fingerprint/', views.fingerprint_song, name='fingerprint_song'),
] 