from django.urls import path
from .views import UserView

urlpatterns = [
    path('users/create', UserView.create, name='user-create'),
    path('users/update/<int:id>', UserView.update, name='user-update'),
    path('users', UserView.get_all, name='user-get-all'),
    path('users/<int:id>', UserView.get_one, name='user-get-one'),
]