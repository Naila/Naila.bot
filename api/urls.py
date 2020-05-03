from django.urls import include, path
from rest_framework import routers
from .api_views import *
from webhooks.api_views import GithubWebhooks


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("ship", Ship.as_view(), name="ship"),
    path("webhook/github", GithubWebhooks.as_view(), name="webhook/github"),
    path("api-auth/", include("rest_framework.urls"))
]
