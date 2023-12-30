from django.urls import path
from .views import UserView

urlpatterns = [
    path('users/create', UserView.create, name='user-create'),
    path('users/update/<int:id>', UserView.update, name='user-update'),
    path('users', UserView.get_all, name='user-get-all'),
    path('users/<int:id>', UserView.get_one, name='user-get-one'),


    path('company/users/create', UserView.company_user_create, name='com-user-create'),
    path('company/users', UserView.company_user_get_all, name='com-user-get-all'),

    path('upload', UserView.upload_file, name='upload-file'),

    path('test', UserView.as_view(), name='test')
]