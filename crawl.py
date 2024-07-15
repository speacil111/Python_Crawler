import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import re
from fake_useragent import UserAgent
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from requests.exceptions import ProxyError


def get_song(url):
    songs={'name':[],'singer':[],'cover':[],'url':[],'lyric':[],'singer_id':[]}
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        ,'Referer':'https://music.163.com/'
        
    }

    url=url

    response = requests.get(url=url,headers=headers)
    html=response.text
    song_list=re.findall('<li><a href="/song\?id=(.*?)">(.*?)</a></li>',html)
    for song in song_list:
        #歌曲名、歌手名
        url_song=f'https://music.163.com/song?id={song[0]}'
        url_lyric= f'https://music.163.com/api/song/media?id={song[0]}'
        print(url_lyric)
        response1=requests.get(url=url_song,headers=headers)
        time.sleep(random.randint(1,2))
        soup1=BeautifulSoup(response1.text,'html.parser')
        singer_name=soup1.find('a',class_='s-fc7',href=re.compile(r'/artist\?id=\d+'))
        if singer_name:
            singer=singer_name.text
        else:
            singer='未知'
        #爬取歌词
        response2=requests.get(url=url_lyric,headers=headers)
        response2.encoding=response2.apparent_encoding
        r2json=json.loads(response2.text)
        try:
            lyric=r2json['lyric']
            lyric_text = re.sub(r'\[\d+:\d+\.\d+\]', '', lyric)
            print(lyric_text)
        except requests.exceptions.ProxyError as e:
            print(f"代理错误: {e}")
        except requests.exceptions.Timeout as e:
            print(f"请求超时: {e}")
        except Exception as e:
            lyric_text = '暂时无歌词'
            print(lyric_text)
        #封面
        cover=soup1.select('div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cvrwrap.f-cb.f-pr > div.u-cover.u-cover-6.f-fl > img')
        if cover:
            cover_image_src = cover[0].get('src')

        else:
            cover_image_src='无封面'
        #爬取歌手id,只保留一个
        singer_id=soup1.find('a',class_='s-fc7',href=re.compile(r'/artist\?id=\d+'))

        if singer_id:
            singer_id=singer_id.get('href')
            singer_id=re.findall(r'/artist\?id=(\d+)',singer_id)
            singer_id=singer_id[0]
        else:
            singer_id='未知id'
        #保存至字典
        if song[1] not in songs['name']:
            songs['name'].append(song[1])
            songs['singer'].append(singer)
            songs['cover'].append(cover_image_src)
            songs['url'].append(url_song)
            songs['lyric'].append(lyric_text)
            songs['singer_id'].append(singer_id)

    #保存至csv
    data=pd.DataFrame(songs,columns=['name','singer','cover','url','lyric','singer_id'])
    data.to_csv('song.csv',mode='a',encoding='utf-8',index=False,header=False)



def get_singer():
    singer={'name':[],'cover':[],'url':[],'singer_id':[],'intro':[]}
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
    }
    data=pd.read_csv('song.csv')
    id=data['singer_id']
    #最好分组爬取
    for singer_item in id:
        url_singer=f'https://music.163.com/artist?id={singer_item}' #歌手原始url
        print(url_singer)
        try:
            response1=requests.get(url=url_singer,headers=headers)
        except requests.exceptions.ConnectTimeout:
            print("连接超时"+url_singer)
            continue
        except requests.exceptions.ReadTimeout:
            print("读取超时"+url_singer)
            continue
        except requests.exceptions.RequestException as e:
            print("请求异常:", e)
            print("请求异常"+url_singer)
            continue
        time.sleep(1)
        soup_singer=BeautifulSoup(response1.text,'html.parser')

        #歌手名
        singer_name=soup_singer.find('h2',id="artist-name").text
        cover=soup_singer.select('div.g-bd4.f-cb > div.g-mn4 > div > div > div.n-artist.f-cb > img')
        if cover:
            cover_image_src = cover[0].get('src')

        else:
            cover_image_src='无封面'

        #歌手简介   
        url_intro=f'https://music.163.com/artist/desc?id={singer_item}'
        response2=requests.get(url=url_intro,headers=headers)
        soup2=BeautifulSoup(response2.text,'html.parser')
        try:
            intro_text=soup2.select(' div.g-bd4.f-cb > div.g-mn4 > div > div > div:nth-child(3) > div > p')
            intro_text=intro_text[0].text.strip()
        except Exception as e:
            intro_text='暂无简介'
        #保存至字典
        if singer_name not in singer['name']:
            singer['name'].append(singer_name)
            singer['singer_id'].append(singer_item)
            singer['cover'].append(cover_image_src)
            singer['url'].append(url_singer)
            singer['intro'].append(intro_text)
    #保存至csv

    data=pd.DataFrame(singer,columns=['name','cover','url','intro','singer_id '])
    data.to_csv('singer.csv',mode='a',encoding='utf-8',index=False,header=False)


def get_urls():
    urls=[]
    url='https://music.163.com/discover/toplist'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        ,'Referer':'https://music.163.com/'
        
    }
    response=requests.get(url=url,headers=headers)
    soup=BeautifulSoup(response.text,'html.parser')
    url_list=soup.find_all('a',href=re.compile(r'/discover/toplist\?id=\d+'),class_='s-fc0')
    for url in url_list:
        urls.append(url.get('href'))
    with open('urls.txt','w',encoding='utf-8') as f:
        for url in urls:
            f.write(url+'\n')
    return urls

def get_song_by_lists(url):
    songs={'name':[],'singer':[],'cover':[],'url':[],'lyric':[],'singer_id':[]}
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        ,'Referer':'https://music.163.com/'
        
    }
    url=url
    response = requests.get(url=url,headers=headers)
    html=response.text
    soup1=BeautifulSoup(html,'html.parser')
    id_list=soup1.find_all('a',class_='msk')

    for id in id_list:
        url0=f'https://music.163.com{id.get("href")}'
        response0=requests.get(url=url0,headers=headers)
        html2=response0.text
        song_list=re.findall('<li><a href="/song\?id=(.*?)">(.*?)</a></li>',html2)
        for song in song_list:
            #歌曲名、歌手名
            url_song=f'https://music.163.com/song?id={song[0]}'
            url_lyric= f'https://music.163.com/api/song/media?id={song[0]}'
            print(url_lyric)
            response1=requests.get(url=url_song,headers=headers)
            time.sleep(random.randint(1,2))
            soup1=BeautifulSoup(response1.text,'html.parser')
            singer_name=soup1.find('a',class_='s-fc7',href=re.compile(r'/artist\?id=\d+'))
            if singer_name:
                singer=singer_name.text
            else:
                singer='未知'
            #爬取歌词
            response2=requests.get(url=url_lyric,headers=headers)
            response2.encoding=response2.apparent_encoding
            r2json=json.loads(response2.text)
            try:
                lyric=r2json['lyric']
                lyric_text = re.sub(r'\[\d+:\d+\.\d+\]', '', lyric)
                print(lyric_text)
            except requests.exceptions.ProxyError as e:
                print(f"代理错误: {e}")
            except requests.exceptions.Timeout as e:
                print(f"请求超时: {e}")
            except Exception as e:
                lyric_text = '暂时无歌词'
                print(lyric_text)
            #封面
            cover=soup1.select('div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cvrwrap.f-cb.f-pr > div.u-cover.u-cover-6.f-fl > img')
            if cover:
                cover_image_src = cover[0].get('src')

            else:
                cover_image_src='无封面'
        #爬取歌手id,只保留一个
            singer_id=soup1.find('a',class_='s-fc7',href=re.compile(r'/artist\?id=\d+'))

            if singer_id:
                singer_id=singer_id.get('href')
                singer_id=re.findall(r'/artist\?id=(\d+)',singer_id)
                singer_id=singer_id[0]
            else:
                singer_id='未知id'
            #保存至字典
            if song[1] not in songs['name']:
                songs['name'].append(song[1])
                songs['singer'].append(singer)
                songs['cover'].append(cover_image_src)
                songs['url'].append(url_song)
                songs['lyric'].append(lyric_text)
                songs['singer_id'].append(singer_id)


            # #所有都保存至csv
            # data=pd.DataFrame({'歌曲名':[song[1]],'歌手名':[singer],'封面':[cover_image_src],'歌曲链接':[url1],'歌词':[lyric_text],})
            # data.to_csv('song.csv',mode='a',encoding='utf-8',index=False,header=False)
            # #以json格式储存
            # with open('song.json','a',encoding='utf-8') as f:
            #     json.dump({'歌曲名':song[1],'歌手名':singer,'封面':cover_image_src,'歌曲链接':url1,'歌词':lyric_text},f,ensure_ascii=False)
            
        #保存至csv
    data=pd.DataFrame(songs,columns=['name','singer','cover','url','lyric','singer_id'])
    data.to_csv('song.csv',mode='a',encoding='utf-8',index=False,header=False)



if __name__ == '__main__':
    #重置csv文件
    # columns = ['name', 'singer', 'cover', 'url', 'lyric','singer_id']
    # data = pd.DataFrame(columns=columns)
    # data.to_csv('song.csv', mode='w', encoding='utf-8', index=False)
    # columns2=['name','cover','url','intro','singer_id']
    # data2=pd.DataFrame(columns=columns2)
    # data2.to_csv('singer.csv',mode='w',encoding='utf-8',index=False)
    urls=get_urls()
    for id in urls:
        url=f'https://music.163.com{id}'
        get_song(url)   # 爬歌词需要url，歌手不需要
    get_song_by_lists('https://music.163.com/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=70')
    get_singer() #需要爬取song.csv中的singer_id
    print('爬取完成')
