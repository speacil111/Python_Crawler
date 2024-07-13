from music.models import Song, Comment,Singer
from django.shortcuts import render ,get_object_or_404, redirect
from django.template import Context, loader
from django.http import HttpResponse,  HttpResponseRedirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
# Create your views here.
def song_list(request):
    songs=Song.objects.all()
    paginator=Paginator(songs,20)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)
    return render(request,'music/song_list.html',{'page_obj':page_obj,'songs':songs})

def song_detail(request,id):
    song=Song.objects.get(song_id=id)
    comments=song.comment_set.all()
    if request.method == 'POST':
        comment_content = request.POST.get('comment_content')
        if comment_content:
            Comment.objects.create(song=song, comment_content=comment_content,
                                   create_time=timezone.now())
            return HttpResponseRedirect(f'/song/{id}/')
        else:
            return render(request,'music/song.html',{'song':song,'comments':comments})
    return render(request,'music/song.html',{'song':song,'comments':comments})
def comment(request,id):
    data=request.POST
    comment_content=data['comment_content']
    song=Song.objects.get(song_id=id)
    obj=Comment(song=song,comment_content=comment_content) 
    obj.full_clean()
    obj.save()
    return HttpResponseRedirect(f'song/{id}/')

def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        song_id = comment.song.song_id
        comment.delete()
        return HttpResponseRedirect(f'/song/{song_id}/')
    else:
        return HttpResponseRedirect('/')
def singer_list(request):
    singers=Singer.objects.all()
    paginator=Paginator(singers,20)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)
    return render(request,'music/singer_list.html',{'page_obj':page_obj,'singers':singers})

def singer_detail(request,id):
    singer=Singer.objects.get(self_id=id)
    context_singer={
        'name':singer.name,
        'cover':singer.cover,
        'intro':singer.intro,
        'original_url':singer.original_url,
        'self_id':singer.self_id,
    }
    Songs=Song.objects.filter(singer_id=id)
    return render(request,'music/singer.html',{'singer':context_singer,'Songs':Songs})

def search(request):
    start_time=timezone.now()
    query=request.GET.get('query')
    search_type=request.GET.get('type')
    if search_type=='song':
        songs=Song.objects.filter(Q(name__contains=query)|Q(singer__contains=query)|Q(lyric__contains=query))
        paginator=Paginator(songs,20)
        page_num=request.GET.get('page')
        page_obj=paginator.get_page(page_num) 
        end_time=timezone.now()
        search_time=end_time-start_time
        search_time=search_time.total_seconds()
        search_number=len(songs)
        if songs.exists():
            return render(request, 'music/song_list.html', {'page_obj': page_obj, 'songs': songs, "query": query, "type": search_type,
                                                         'search_time':search_time,'search_number':search_number})
        else:
            referer = request.META.get('HTTP_REFERER', '/')
            separator = '&' if '?' in referer else '?'
            return HttpResponseRedirect(f'{referer}{separator}no_results=true&search_time={search_time}')

    elif search_type=='singer':
        singers=Singer.objects.filter(Q(name__contains=query)|Q(intro__contains=query))
        paginator=Paginator(singers,20)
        page_num=request.GET.get('page')
        page_obj=paginator.get_page(page_num)
        end_time=timezone.now()
        search_time=end_time-start_time
        search_time=search_time.total_seconds()
        if singers.exists():
            return render(request,'music/singer_list.html',{'page_obj':page_obj,'singers':singers,"query":query,"type":search_type,
                                                          'search_time':search_time,'search_number':len(singers)})
        else:
            referer = request.META.get('HTTP_REFERER', '/')
            separator = '&' if '?' in referer else '?'
            return HttpResponseRedirect(f'{referer}{separator}no_results=true&search_time={search_time}')
    else:

        referer = request.META.get('HTTP_REFERER', '/')
        separator = '&' if '?' in referer else '?'
        return HttpResponseRedirect(f'{referer}{separator}error=true&search_time={search_time}')
