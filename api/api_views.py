import os
import random
from io import BytesIO

import requests
import requests_cache
from PIL import Image
from django.http import FileResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from nailabot import settings

# Cache all requests for 5 minutes to prevent rate limiting by Discord
requests_cache.install_cache(expire_after=300, include_get_headers=True)


class Ship(APIView):
    """
    This endpoint returns an image for two given user avatars on either side of a random heart
    """

    # permission_classes = [IsAuthenticated]

    def get_avatars(self):
        avatar1 = self.request.GET.get("avatar1", None)
        avatar2 = self.request.GET.get("avatar2", None)

        if avatar1 and avatar2:
            with requests_cache.disabled():
                avatar1 = Image.open(
                    requests.get(avatar1, stream=True).raw
                ).resize((200, 200), Image.LANCZOS).convert("RGBA")
                avatar2 = Image.open(
                    requests.get(avatar2, stream=True).raw
                ).resize((200, 200), Image.LANCZOS).convert("RGBA")

            return avatar1, avatar2

        return None, None

    def get(self, request):
        avatar1, avatar2 = self.get_avatars()

        if not avatar1 or not avatar2:
            return Response({
                "message": "You need to provide avatar1 and avatar2 as kwargs"
            }, status=status.HTTP_400_BAD_REQUEST)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, "assets/images/ship/" if settings.DEBUG else "static/images/ship/")
        background = Image.new("RGBA", (600, 200), (0, 0, 0, 0))
        heart = Image.open(path + random.choice([x for x in os.listdir(path)])).convert("RGBA")
        background.paste(avatar1, (0, 0), avatar1)
        background.paste(heart, (201, 0), heart)
        background.paste(avatar2, (401, 0), avatar2)
        temp_image = BytesIO()
        background.save(temp_image, "PNG")
        temp_image.seek(0)
        response = FileResponse(temp_image, filename="ship.png")
        return response


class CreateDeleteRefreshApiKey(APIView):
    """
    Creates, deletes, or refreshes an API key
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, action):
        if action == "create":
            token = Token.objects.get_or_create(user=request.user)
            return Response({"token": token[0].key}, status=status.HTTP_201_CREATED)
        if action == "delete":
            token = Token.objects.get_or_create(user=request.user)[0]
            token.delete()
            return Response(status=status.HTTP_200_OK)
        if action == "refresh":
            old_token = Token.objects.get_or_create(user=request.user)[0]
            old_token.delete()
            token = Token.objects.get_or_create(user=request.user)
            return Response({"token": token[0].key}, status=status.HTTP_200_OK)
