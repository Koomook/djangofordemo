from rest_framework import serializers
from musicus.models import Song, Lyrics


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'song', 'extention')
    
class LyricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyrics
        fields = ('id', 'extention', 'lyrics', 'outputs', 'keyword', 'inputs') #  일부러 inputs_idx 빼봄.