from snippets.models import Snippet, Hello
from snippets.serializers import SnippetSerializer, HelloSerializer
from rest_framework import generics
# to make hello:world
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class HelloList(APIView):
    def get(self, request, format=None):
        # hello = Hello.objects.all()
        # serializer = HelloSerializer(hello, many=True)
        return Response({'hello':'world'}, status=status.HTTP_204_NO_CONTENT)
