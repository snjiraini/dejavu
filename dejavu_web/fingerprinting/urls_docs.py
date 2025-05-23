from django.urls import path
from . import views_docs

urlpatterns = [
    path('', views_docs.api_overview, name='api_overview'),
]
