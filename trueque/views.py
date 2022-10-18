
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class Health(APIView):
    """Check avaiability"""

    def get(self, request):
        return Response({"message": "ok"}, status=status.HTTP_200_OK)
