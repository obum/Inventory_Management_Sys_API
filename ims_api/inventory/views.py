from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, InventoryChangeSerializer, InventoryItemSerializer
from .models import Category, InventoryChange, InventoryItem
from rest_framework import permissions, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .permissions import IsOwnerorReadonly
from django_filters import rest_framework as filter
# Create your views here.

User = get_user_model()

class ItemFilter(filter.FilterSet):
    min_price = filter.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filter.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = InventoryItem
        fields = ['category', 'max_price', 'min_price', 'low_stock']

class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class InventoryItemViewset(ModelViewSet):
    # Only authenticated users should be able to manage inventory (i.e., create, update, or delete items)
    permission_classes = [IsOwnerorReadonly]
    serializer_class = InventoryItemSerializer
    queryset = InventoryItem.objects.all()
    filter_backends = (filter.DjangoFilterBackend, filters.OrderingFilter) # Add sorting functionality
    filterset_class = ItemFilter
    ordering_fields = ['name', 'quantity', 'price', 'created_at']

    # def get_queryset(self):
    #     # Ensure that logged_in_users can only access their own inventory items
    #     queryset = InventoryItem.objects.filter(owner=self.request.user)
    #     return queryset   

class InventoryLevelView(generics.ListAPIView):
    permission_classes = [IsOwnerorReadonly]
    serializer_class = InventoryItemSerializer
    queryset = InventoryItem.objects.all()
    filter_backends = (filter.DjangoFilterBackend, filters.OrderingFilter) # Add sorting functionality
    filterset_class = ItemFilter
    ordering_fields = ['name', 'quantity', 'price', 'created_at']
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = InventoryItemSerializer(queryset, many=True)
        items = serializer.data
  
        inventory_level = [
            {
                "id": item['id'],
                "name": item["name"],
                "quantity": item["quantity"]
            }
            for item in items
        ]
              
        return Response(
                inventory_level,
                status=status.HTTP_200_OK
            )

class InventoryChangeViewSet(ModelViewSet):
    """A viewset to handle inventory changes."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InventoryChangeSerializer
    queryset = InventoryChange.objects.all()

    # Upon creation set the logged_in user as the changed_by value
    def perform_create(self, serializer):
        serializer.save(changed_by=self.request.user)

    # Define a custom action to display all changes on an item
    @action(methods=['get'], detail=True, url_path='history', url_name='inventory_change_history')
    def history(self, request, pk=None):
        """Action to view the inventory change history of a specific item."""
        item_id = pk
        changes = InventoryChange.objects.filter(inventory_item__id=item_id).order_by('created_at')
        inventory_item = changes.first().inventory_item # get the first change and get the item associated with it
        inventory_item_name = inventory_item.name
        serializer = self.get_serializer(changes, many=True)
        data = serializer.data

        return Response(
            {
                'inventory_item_name': inventory_item_name,
                'change history': data
            },
            status=status.HTTP_200_OK
        )
 