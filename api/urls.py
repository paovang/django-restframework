# from django.urls import path
# from .views import getAll, getOne, create, update

# urlpatterns = [
#     path('users', getAll),
#     path('users/<int:id>', getOne),
#     path('user/create', create),
#     path('user/update/<int:id>', update),
# ]

# from django.urls import path
# from .views import UserView

# urlpatterns = [
#     path('create/', UserView.as_view({'post': 'create'}), name='user-create'),
#     path('update/<int:id>/', UserView.as_view({'put': 'update'}), name='user-update'),
#     path('getAll/', UserView.as_view({'get': 'get_all'}), name='user-get-all'),
#     path('getOne/<int:id>/', UserView.as_view({'get': 'get_one'}), name='user-get-one'),
# ]

from django.urls import path
from .views import UserView

urlpatterns = [
    path('users/create', UserView.create, name='user-create'),
    path('users/update/<int:id>', UserView.update, name='user-update'),
    path('users', UserView.get_all, name='user-get-all'),
    path('users/<int:id>', UserView.get_one, name='user-get-one'),
]