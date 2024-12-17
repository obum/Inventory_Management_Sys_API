from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
# Create your models here.

class UserManager(BaseUserManager):
    # defines the methods for creating users
    
    def create_user(self, email, username, role, password=None):
        if not (email and username):
            raise ValueError("Users must have an email address and username")
        
        email=self.normalize_email(email) # normalize the email 
        # creates an instance of the user model in memory
        user: AbstractUser = self.model(
            email = email,
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        
        if role == 'Admin':
            user.is_staff = True
        
        return user
        
        
    def createsuperuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username,
            password=password
            )
        
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user    

class User(AbstractUser):
    # define additional fields your require from a user
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STOREKEEPER = 'STOREKEEPER', 'StoreKeeper'
        MANAGER = 'MANAGER', 'Manager'
    
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)
    role = models.CharField(
        max_length=12,
        choices=Roles.choices,
        default=Roles.STOREKEEPER,
    )
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = UserManager()