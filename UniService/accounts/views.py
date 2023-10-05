from rest_framework import viewsets
from rest_framework import permissions
from accounts.serializers import UserSerializer
from accounts.models import User


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.AllowAny]
    filterset_fields = [
        "type",
        "first_name",
        "last_name",
        "dob",
        "is_active",
    ]