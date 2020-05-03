from rest_framework.views import APIView


class Webhooks(APIView):
    def post(self, request):
        print(request.headers)
