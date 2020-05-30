from django.urls import path
from .views import BanlistHomeView

urlpatterns = [
    path("", BanlistHomeView.as_view(), name="BanlistHomeView")
]
