from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MemberCardSerializer
from .models import MemberCard


class MemberCardViewSet(viewsets.ModelViewSet):
    queryset = MemberCard.objects.all().order_by("-card_num")
    serializer_class = MemberCardSerializer
    # permission_classes = [permissions.AllowAny]
    search_fields = ["=user_id"]
    filterset_fields = ["user_id"]


def index(requests) -> HttpResponse:
    context = {}
    return render(requests, "members_card/index.html", context)
