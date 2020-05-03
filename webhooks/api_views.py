import hmac
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GithubWebhooks(APIView):
    def post(self, request):
        secret = os.getenv("GITHUB-SECRET")
        header_signature = request.headers.get("X-Hub-Signature")
        sha_name, signature = header_signature.split("=")
        if sha_name != "sha1":
            return Response({"message": "sha1 required"}, status=status.HTTP_400_BAD_REQUEST)
        mac = hmac.new(str(secret), msg=request.data, digestmod="sha1")
        if not str(mac.hexdigest() == str(signature)):
            return Response({"message": "invalid secret"}, status=status.HTTP_403_FORBIDDEN)

        event = request.headers.get("X-GitHub-Event", "ping")
        if event == "ping":
            return Response("Pong!")

        print(event)
        print(request.data)
