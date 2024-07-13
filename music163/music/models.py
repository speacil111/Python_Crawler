from django.db import models
from django.utils import timezone
# Create your models here.

class Song(models.Model):
    name = models.CharField(max_length=30)
    singer = models.CharField(max_length=30)
    cover = models.URLField(max_length=200)
    original_url = models.URLField(max_length=200)
    lyric = models.CharField(max_length=1000)
    singer_id = models.CharField(max_length=20)
    song_id = models.CharField(max_length=20)

class Comment(models.Model):
    song= models.ForeignKey(Song, on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=200)
    create_time = models.DateTimeField()
    class Meta:
        ordering = ['-create_time']

class Singer(models.Model):
    name = models.CharField(max_length=30)
    self_id = models.CharField(max_length=30)
    cover = models.URLField(max_length=200)
    intro= models.CharField(max_length=1000)
    original_url= models.URLField(max_length=200)
class Search(models.Model): 
    keyword = models.CharField(max_length=20)
    search_time = models.DateTimeField()
    def __str__(self):
        return self.keyword