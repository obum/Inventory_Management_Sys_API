from django.urls import path
from .views import UserRegistrationView, UserDetailUpdateView, UserAllDetailUpdateView, UserListView, UserLogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='users-list'), 
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserDetailUpdateView.as_view(), name='user-detail-update'),
    path('<int:pk>/', UserAllDetailUpdateView.as_view(), name='user-detail-update-delete'),
    # path('', UserListView.as_view(), name='users'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', UserLogoutView.as_view(), name='logout')
]