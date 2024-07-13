from django.urls import path   #导入路径相关配置
from music import  views  #导入视图views

urlpatterns = [  #路径配置
    path('song_list/', views.song_list, name='song_list'),
    path('song/<int:id>/', views.song_detail, name='song_detail'),
    path('singer_list/', views.singer_list, name='singer_list'),
    path('singer/<int:id>/', views.singer_detail, name='singer_detail'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('search/', views.search, name='search')

]
