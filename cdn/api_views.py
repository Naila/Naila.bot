from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class CDNArchive(APIView):
    def get_file(self):
        my_file = self.request.FILES.get("file", None)
        if my_file and my_file.name:
            return my_file
        return None

    def post(self, request):
        file = self.get_file()
        if not file:
            return Response({"message": "You must provide a valid file!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Success!", "filename": file.name})
