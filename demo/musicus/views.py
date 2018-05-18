from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

# test serializer
from django.db.models import Max
import random
from musicus.models import Song, Lyrics
from musicus.serializers import SongSerializer, LyricsSerializer

# from .src.song import pickmp3
# from .src.lyrics import Models
# from .src.lyrics_gen import Gen
# batch_size = 3
# model = Models(batch_size=batch_size)
# gen = Gen()

# with open('musicus/src/meta.json') as fp:
#     meta = json.load(fp)
# K2L_kor_infer = model.load_K2L_kor(
#     meta['K2L_kor_project'], meta['K2L_kor_dir_path'], 0.8)
# S2S_kor_infer = model.load_S2S_kor(
#     meta['S2S_kor_project'], meta['S2S_kor_dir_path'], 0.8)


class Hello(APIView):
    """
    test api
    """

    def get(self, request, format=None):
        print(request.data)
        return Response(data={'hello': 'pozalabs'}, status=status.HTTP_200_OK)


class SongList(APIView):
    """List all songs, or create a new song."""

    def get(self, request, format=None):
        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
    
    def post(self, request, format=None):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SongDetail(APIView):
    """Retrieve, update or delete a song instance"""

    def get_object(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise Http404

    def get_random(self):
        """ref: https://books.agiliq.com/projects/django-orm-cookbook/en/latest/random.html"""
        max_id = Song.objects.all().aggregate(max_id=Max("id"))['max_id']
        # model has deletions, so loop until valid song is picked
        while True:
            pk = random.randint(1, max_id)
            song = self.get_object(pk)
            return song
    
    def get(self, request, pk, format=None):
        song = self.get_random()
        serializer = SongSerializer(song)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        song = self.get_object(pk)
        serializer = SongSerializer(song)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        song = self.get_object(pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class Lyrics(APIView):
    """generate lyrics"""

    def get(self, request, language, ver, slug, format=None):
        print(language, type(language))
        print(ver, type(ver))
        print(slug, type(slug))
        keyword_input = slug
        if language == 'kor' and ver == '02':
            spaced_lyrics = gen.generate_kor02(
                keyword_input, S2S_kor_infer, K2L_kor_infer, batch_size=batch_size, appending_size=2)
            return Response({'lyrics': spaced_lyrics}, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
        else:
            return Response(Http404)
