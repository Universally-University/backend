from datetime import datetime
from rest_framework import viewsets
from rest_framework import permissions
from accounts.serializers import UserSerializer
from accounts.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponse


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = [
        "type",
        "first_name",
        "last_name",
        "dob",
        "is_active",
    ]


def set_cookie(
    response: HttpResponse,
    key: str,
    value: str,
    max_age: int | None = None,
    expires: str | datetime | None = None,
):
    response.set_cookie(key, value, max_age, expires)
    return response


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...

