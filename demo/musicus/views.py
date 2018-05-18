# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .src.song import pickmp3

from .src.lyrics_core import load_model, generate
batch_size = 3
K2L_kor_infer, S2S_kor_infer = load_model(batch_size=batch_size)

class Hello(APIView):
    """
    test api
    """
    def get(self, request, format=None):
        print(request.data)
        return Response(data={'hello': 'pozalabs'}, status=status.HTTP_200_OK)


class Song(APIView):
    """pick random song"""
    def get(self, request, format=None):
        mp3 = pickmp3()
        return Response({'song': mp3}, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})

class Lyrics(APIView):
    """generate lyrics"""
    def get(self, request, slug, format=None):
        print(slug)
        keyword_input = slug
        spaced_lyrics = generate(keyword_input, S2S_kor_infer, K2L_kor_infer,
                                        batch_size=batch_size, appending_size=2)

        return Response({'lyrics':spaced_lyrics})
        
        

