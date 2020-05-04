import hashlib
import hmac
import json
import os

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GithubWebhooks(APIView):
    def validate_request(self) -> bool:
        secret = os.getenv("GITHUB_SECRET")
        header_signature = self.request.headers.get("X-Hub-Signature")
        signature = header_signature.split("=")[1]

        mac = hmac.new(str.encode(secret), msg=json.dumps(self.request.data).encode("utf8"), digestmod=hashlib.sha1)
        if not str(mac.hexdigest() == str(signature)):
            return False
        return True

    def post(self, request):
        valid = self.validate_request()
        if not valid:
            return Response({"message": "Could not validate request!"}, status=status.HTTP_403_FORBIDDEN)

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
            author_name = action
            color = 16711680
            if action == "created":
                author_name = "New Sponsor!"
                color = 65370
            webhook_data = {
                "username": "GitHub Sponsor",
                "avatar_url": "https://kanin.naila.bot/2020/05/04/tPy1JU.png",
                "embeds": [{
                    "timestamp": created,
                    "color": color,
                    "thumbnail": {
                        "url": sponsor_data["avatar_url"]
                    },
                    "author": {
                        "name": author_name,
                        "url": f"https://github.com/sponsors/{maintainer_data['login']}",
                        "icon_url": maintainer_data["avatar_url"]
                    },
                    "fields": [
                        {
                            "name": "Sponsor:",
                            "value": f"**[{sponsor_data['login']}]({sponsor_data['html_url']})**"
                        },
                        {
                            "name": "Tier:",
                            "value": f"**Name:** {tier_data['name']}\n"
                                     f"**Price:** ${tier_data['monthly_price_in_dollars']}"
                        }
                    ]
                }]
            }
            if public:
                requests.post(url=os.getenv("GITHUB_SPONSORS_WEBHOOK_PUBLIC"), json=webhook_data)
            else:
                requests.post(url=os.getenv("GITHUB_SPONSORS_WEBHOOK_PRIVATE"), json=webhook_data)
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(event)


class PatreonWebhooks(APIView):
    def post(self, request):
        print(request.data)
        print(request.headers)
