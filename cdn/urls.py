from django.urls import path
from .views import CDNView
from .api_views import *

urlpatterns = [
    path("", CDNView.as_view(), name="CDN"),
    path("upload/archive", CDNArchive.as_view()),
]
