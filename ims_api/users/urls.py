from django.urls import path
from .views import UserRegistrationView, UserDetailUpdateView, UserAllDetailUpdateView, UserListView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserDetailUpdateView.as_view(), name='user-detail-update'),
    path('<int:pk>/', UserAllDetailUpdateView.as_view(), name='user-detail-update-delete'),
    path('', UserListView.as_view(), name='users'),

]