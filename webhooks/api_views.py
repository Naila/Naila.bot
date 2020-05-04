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
        header_signature = self.request.headers.get("X-Hub-Signature", None)
        if header_signature is None:
            return False

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
            tier_data = request.data["sponsorship"]["tier"]
            sponsor_data = request.data["sponsorship"]["sponsor"]
            old_tier_data = None
            maintainer_data = request.data["sponsorship"]["maintainer"]
            author_name = action
            color = 16711680
            if action in ["pending_cancellation", "pending_tier_change"]:
                return Response(status=status.HTTP_204_NO_CONTENT)
            if action == "created":
                author_name = "New Sponsor!"
                color = 65370
            elif action == "cancelled":
                author_name = "Sponsorship Cancelled!"
                color = 16711680
            elif action == "tier_changed":
                author_name = "Sponsorship Edited!"
                color = 65370
                old_tier_data = request.data["changes"]["tier"]["from"]
                if old_tier_data["monthly_price_in_cents"] > tier_data["monthly_price_in_cents"]:
                    color = 16763904
            webhook_data = {
                "username": "GitHub Sponsor",
                "avatar_url": "https://kanin.naila.bot/2020/05/04/tPy1JU.png",
                "embeds": [{
                    "timestamp": request.data["sponsorship"]["created_at"],
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

            if old_tier_data is not None:
                webhook_data["embeds"][0]["fields"].append(
                    {
                        "name": "Old Tier:",
                        "value": f"**Name:** {old_tier_data['name']}\n"
                                 f"**Price:** ${old_tier_data['monthly_price_in_dollars']}"
                    }
                )

            if request.data["sponsorship"]["privacy_level"] == "private":
                requests.post(url=os.getenv("GITHUB_SPONSORS_WEBHOOK_PRIVATE"), json=webhook_data)
            else:
                requests.post(url=os.getenv("GITHUB_SPONSORS_WEBHOOK_PUBLIC"), json=webhook_data)
            return Response(status=status.HTTP_204_NO_CONTENT)

        print(event)
