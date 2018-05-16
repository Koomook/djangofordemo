# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import numpy as np
mp3dir = 'mp3'
mp3s = [os.path.join(mp3dir, fn) for fn in os.listdir(mp3dir)]
print(mp3s)

class Hello(APIView):
    """
    test api
    """
    def get(self, request, format=None):
        return Response(data={'hello':'pozalabs'}, status=status.HTTP_200_OK)

class Song(APIView):
    """pick random song"""
    def get(self, request, format=None):
        selected = np.random.choice(mp3s, 1)[0]
        song = "<audio src='{}' controls controlsList='nodownload'></audio>".format(
            selected)
        return Response({'song':song}, status=status.HTTP_200_OK)
