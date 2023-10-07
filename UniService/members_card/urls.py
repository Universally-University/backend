from django.urls import include, path
from rest_framework import routers
import members_card.views as views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", views.index),
]
