from django.urls import path
from .views import SignupView, LoginView, UserListView, UserDetailView, DataDetailView

urlpatterns = [
    # Authentication
    path('auth/signup', SignupView.as_view(), name='signup'),
    path('auth/login', LoginView.as_view(), name='login'),

    # User Management
    path('users', UserListView.as_view(), name='user-list'),  # Admin only for GET all users
    path('users/<int:id>', UserDetailView.as_view(), name='user-detail'),  # GET, PUT, DELETE user

    # Data Management
    path('data', DataDetailView.as_view(), name='data-list'),  # GET, POST for data
    path('data/<int:id>', DataDetailView.as_view(), name='data-detail'),  # PUT, DELETE for data
]
