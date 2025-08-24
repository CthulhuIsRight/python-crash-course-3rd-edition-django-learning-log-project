"""Defines URL patterns for learning_logs_app"""
from django.urls import path
from . import views

app_name = 'learning_logs_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
]