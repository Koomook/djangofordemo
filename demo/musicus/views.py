# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.song import picksong


class Hello(APIView):
    """
    test api
    """
    def get(self, request, format=None):
        return Response(data={'hello':'pozalabs'}, status=status.HTTP_200_OK)

class Song(APIView):
    """pick random song"""
    def get(self, request, format=None):
        song = picksong()
        return Response({'song':song}, status=status.HTTP_200_OK)