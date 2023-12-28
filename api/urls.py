from django.urls import path
from . import views

urlpatterns = [
    path('users', views.getAll),
    path('users/<int:id>', views.getOne),
    path('user/create', views.create)
]