from django.urls import path
from .views import Minecraft

urlpatterns = [
    path("", Minecraft.as_view(), name="Minecraft")
]
