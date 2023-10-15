from accounts.models import User
from api.serializer import UserSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response
