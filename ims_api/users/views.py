from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, DestroyAPIView
from .serializers import UserSerializer, UserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, generics
# Create your views here.

User = get_user_model()

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    
class UserDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Return the currently logged-in userP
        return self.request.user
    
    # def get_queryset(self):
    #     # Ensure that loogin user can only retrieve and update its own data
    #     logged_in_user = self.request.user
    #     queryset = User.objects.filter(id=logged_in_user.id)
    #     return queryset
    
class UserAllDetailUpdateView(RetrieveUpdateDestroyAPIView): # This view wxpwcts a pk and as such cannot handle retrieving all users
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
class UserLogoutView(DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        
        # Get the refresh token from the body of the HTTP request
        refresh_token = request.data.get('refresh')
        
        # validate the referesh_token parsed
        if not refresh_token:
            return Response(
                {"detail": "Refresh tken required."},
                status= status.HTTP_400_BAD_REQUEST
            )
        try:
            # Blacklist the refresh token  
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status= status.HTTP_400_BAD_REQUEST
            )
