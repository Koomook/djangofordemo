from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from .src.song import pickmp3
from .src.lyrics import Models
from .src.lyrics_gen import Gen
batch_size = 3
model = Models(batch_size=batch_size)
gen = Gen()

with open('musicus/src/meta.json') as fp: # 정말 모르겠군.. 지금 알겠는건 project directory 기준으로 path 됨.
    meta = json.load(fp)
kor_model = model.kor_model()
K2L_kor_infer = model.load_K2L_kor(kor_model, meta['K2L_kor_project'], meta['K2L_kor_dir_path'], 0.8)
S2S_kor_infer = model.load_S2S_kor(kor_model, meta['S2S_kor_project'], meta['S2S_kor_dir_path'], 0.8)


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
        return Response({'song': mp3}, status=status.HTTP_200_OK)


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
            return Response({'lyrics': spaced_lyrics})
        else:
            return Response(Http404)
