from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView, InventoryChangeViewSet, InventoryItemViewset, InventoryLevelView

app_name = 'inventory'

router = DefaultRouter()
router.register(r'', InventoryItemViewset, basename='inventory')
router.register(r'category', CategoryView, basename='category')
router.register(r'changes', InventoryChangeViewSet, basename='inventory-change')


urlpatterns = [
    path('level/', InventoryLevelView.as_view(), name='inventory-level'),
    path('', include(router.urls)),
]

