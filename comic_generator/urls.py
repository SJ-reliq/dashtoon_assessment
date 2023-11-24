from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_comic, name='generate_comic'),
]
