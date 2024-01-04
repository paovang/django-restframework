from django.urls import path
from .views import UserView
# jwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/create', UserView.create, name='user-create'),
    path('users/update/<int:id>', UserView.update, name='user-update'),
    path('users', UserView.get_all, name='user-get-all'),
    path('users/<int:id>', UserView.get_one, name='user-get-one'),


    path('company/users/create', UserView.company_user_create, name='com-user-create'),
    path('company/users', UserView.company_user_get_all, name='com-user-get-all'),

    path('upload', UserView.upload_file, name='upload-file'),

    # jwt
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]