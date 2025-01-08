from django.contrib import admin
from django.urls import path, include
from .views import APIRootView


urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
]
