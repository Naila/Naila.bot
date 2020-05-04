import hashlib
import hmac
import json
import os
from datetime import datetime

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GithubWebhooks(APIView):
    def post(self, request):
        secret = os.getenv("GITHUB_SECRET")
        header_signature = request.headers.get("X-Hub-Signature")
        sha_name, signature = header_signature.split("=")
        if sha_name != "sha1":
            return Response({"message": "sha1 required"}, status=status.HTTP_400_BAD_REQUEST)
        print(type(request.data))
        mac = hmac.new(str.encode(secret), msg=json.dumps(request.data).encode("utf8"), digestmod=hashlib.sha1)
        if not str(mac.hexdigest() == str(signature)):
            return Response({"message": "invalid secret"}, status=status.HTTP_403_FORBIDDEN)

        event = request.headers.get("X-GitHub-Event", "ping")
        if event == "ping":
            return Response("Pong!")

        if event == "sponsorship":
            action = request.data["action"]
            public = "private" not in request.data["sponsorship"]["privacy_level"]
            created = request.data["sponsorship"]["created_at"]
            sponsor_data = request.data["sponsorship"]["sponsor"]
            maintainer_data = request.data["sponsorship"]["maintainer"]
            tier_data = request.data["sponsorship"]["tier"]
            webhook_data = {}
            embed = {
                "timestamp": created,
                "color": 65370,
                "thumbnail": {
                    "url": sponsor_data["avatar_url"]
                },
                "author": {
                    "name": "New sponsor!",
                    "url": f"https://github.com/sponsors/{maintainer_data['login']}",
                    "icon_url": maintainer_data["avatar_url"]
                },
                "fields": [
                    {
                        "name": "Sponsor:",
                        "value": f"[**{sponsor_data['login']}**]({sponsor_data['html_url']})"
                    },
                    {
                        "name": "Tier:",
                        "value": f"**Name:** {tier_data['name']}\n**Price:** ${tier_data['monthly_price_in_dollars']}"
                    }
                ]
            }
            webhook_data["embeds"] = [embed]
            webhook_data["username"] = "GitHub Sponsor"
            webhook_data["avatar_url"] = "https://kanin.naila.bot/2020/05/04/tPy1JU.png"
            requests.post(url=os.getenv("GITHUB_SPONSORS_WEBHOOK"), json=webhook_data)
            return Response("Forwarded!")

        print(event)
