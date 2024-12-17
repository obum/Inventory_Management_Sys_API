from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import UserSerializer, UserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.

User = get_user_model()
class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    
class UserDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Return the currently logged-in user
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