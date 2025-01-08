from rest_framework import serializers
from .models import InventoryChange, InventoryItem, Category
from .models import Category, InventoryItem, ChangeReason

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ChangeReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeReason
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer): 
    # Ensure that only existing categories are used during item creation or serialization.    
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'low_stock']
        # depth = 1
        
    # Ensure validation for required fields like Name, Quantity, and Price.
    def validate_name(self, value):
        # ensure that the item name is not blank
        if not value:
            raise serializers.ValidationError("item name can not be blank")
        # ensure that the item name is unique and is not in the database
        if InventoryItem.objects.filter(name=value).exists():
            raise serializers.ValidationError("item name already exists")
        
        return value  
                
    def validate_quantity(self, value: int):
        if not isinstance(value, int):
            raise serializers.ValidationError("item quantity must be a number") 
        if value < 0:
            raise serializers.ValidationError("item quantity cannot be less than zero")
        
        return value
    
    def validate_price(self, value):
            if value < 0:
                raise serializers.ValidationError("item price can not be less than zero.")
            return value
        
    def create(self, validated_data):
            
        # Ensure the 'owner' field is set to the current user
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError(f"{request.user} is not available.")
                
        validated_data['owner'] = request.user
        inventory_item = InventoryItem.objects.create(**validated_data)
        return inventory_item
    
class InventoryChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryChange
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'changed_by']