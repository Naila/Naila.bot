from django.urls import include, path
from rest_framework import routers
from .api_views import *


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("ship", Ship.as_view(), name="ship"),
    path("api-auth/", include("rest_framework.urls"))
]
