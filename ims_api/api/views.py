from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse('users:users-list', request=request),
            'inventory': reverse('inventory:inventory-list', request=request),
        })