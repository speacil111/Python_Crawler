import pandas as pd
from django.core.management.base import BaseCommand
from music.models import Song,Singer
import csv
from django.db.models import Count

class Command(BaseCommand):
    def handle(self,*args,**options):

        # with open('singer.csv', newline='', encoding='utf-8') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         Singer.objects.create(
        #             self_id=row['singer_id'],
        #             name=row['name'],
        #             cover=row['cover'],
        #             intro=row['intro'],
        #             original_url=row['url'],
        #         )

        # with open('song.csv', newline='', encoding='utf-8') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         Song.objects.create(
        #             name=row['name'],
        #             singer=row['singer'],
        #             cover=row['cover'],
        #             lyric=row['lyric'],
        #             original_url=row['url'],
        #             singer_id=row['singer_id'],
        #             song_id=row['song_id']
        #         )

        # duplicate_song_ids = Song.objects.values('song_id').annotate(song_id_count=Count('id')).filter(song_id_count__gt=1)

        # for entry in duplicate_song_ids:
        #     # 对于每个重复的 song_id，找到所有重复的 Song 对象，但排除第一个
        #     duplicate_songs = Song.objects.filter(song_id=entry['song_id']).order_by('id')[1:]
        #     # 遍历并删除这些重复的 Song 对象
        #     for song in duplicate_songs:
        #         song.delete()


        # 找出重复的 singer_name
        # duplicate_singer_names = Singer.objects.values('name').annotate(name_count=Count('id')).filter(name_count__gt=1)

        # for entry in duplicate_singer_names:
        #     # 对于每个重复的 name，找到所有重复的 Singer 对象，但排除第一个
        #     duplicate_singers = Singer.objects.filter(name=entry['name']).order_by('id')[1:]
        #     # 遍历并删除这些重复的 Singer 对象
        #     for singer in duplicate_singers:
        #         singer.delete()
        
        songs=Song.objects.all()
        print(len(songs))
        singer=Singer.objects.all()
        print(len(singer))
        song=Song.objects.get(song_id='2129666437')
        comment=song.comment_set.all()
        print(comment)
        #无法提交评论