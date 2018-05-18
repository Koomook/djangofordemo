from django.db import models

# Create your models here.
class Song(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    song = models.TextField()
    extention = models.CharField(max_length=10, default='mp3')

    class Meta:
        ordering = ('created',)

class Lyrics(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    extention = models.CharField(max_length=10, default='html')
    lyrics = models.TextField()
    outputs = models.TextField()
    keyword = models.TextField() # or CharField # mysql listfield 쓸 수도 있음.
    inputs = models.TextField()
    inputs_idx = models.TextField()

    class Meta:
        ordering = ('created',)