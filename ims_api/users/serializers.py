from venv import create
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


# Use a dedicated Serializer for user creation
User = get_user_model()
required_fields = ['username', 'email', 'password']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields =  ['id', 'username', 'email', 'role','password', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
        
    role = serializers.ChoiceField(choices=User.Roles.choices, required=False)  # Make 'role' optional

    def validate(self, attrs):
        missing_field = [field for field in required_fields if field not in attrs]
        if missing_field:
            raise ValidationError(f'{missing_field[0]} was not provided')
        return attrs
        
    # Validate the email field to ensure uniqueness  
    def validate_email(self, value):  
        if User.objects.filter(email=value).exists():
            raise ValidationError(f'{value} is already taken')
        return value
    
    # Validate the username field to ensure uniqueness    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError(f'{value} already taken')
        return value
    
    def validate_role(self, attrs):
        if attrs not in [choice[0] for choice in User.Roles.choices]:
            raise serializers.ValidationError(f'Invaid role {attrs}')
        return attrs
    
    # Create a User 
    def create(self, validated_data: dict):    
        # Extract the password field from the validated data
        password = validated_data.pop('password')
        
        # If 'role' is not provided, set it to the default value (STOREKEEPER)
        role = validated_data.get('role', User.Roles.STOREKEEPER)
                
        # Use the User model's manager to create a user instance
        user = User.objects.create_user(
            **validated_data,
            role=role
            )
        
        # Set the password for the user instance (hashing it securely)
        user.set_password(password)
        # Save the user instance to the database
        user.save()

        # Return the created user instance
        return user
    
    # This code is from jwt documentation
    def get_tokens_for_user(self, user):
        # Genterate the JWT token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return {
        'refresh': str(refresh),
        'access': access_token,
        }
        
    def to_representation(self, instance):
        """
        Format the response using the UserSerializer and include the token.
        """
        user_data = super().to_representation(instance)
        user_tokens = self.get_tokens_for_user(instance)
        return {
            'user_info': {
                'id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'role': user_data['role'],
                'creation date': user_data['created_at'],
                'last update': user_data['updated_at'],                
                },
            'refresh_token': user_tokens['refresh'],
            'access_token': user_tokens['access']
        }
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)
    
    class Meta:
        model = User
        fields =  '__all__'
        read_only_fields = ['created_at', 'updated_at']
      
    role = serializers.ChoiceField(choices=User.Roles.choices, required=False)  # Make 'role' optional
        
    def update(self, instance, validated_data:dict):
        instance = super().update(instance, validated_data)
        for key, value in validated_data.items():
            if key != 'password':
                setattr(instance, key, value)
                
        password = validated_data.get('password')
        
        if password:
            # only change the password securely (hashed) if it is not blank.
            instance.set_password(password) 
            
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """
        Format the response using the UserSerializer and include the token.
        """
        user_data = super().to_representation(instance)

        return {
            'user_info': {
                'id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'role': user_data['role'],
                'creation date': user_data['created_at'],
                'last update': user_data['updated_at'],                
                }
            }