import requests
import os
import pandas as pd
import time
def download_image(image_url, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    response = requests.get(image_url,headers=headers,timeout=5)
    time.sleep(1)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print(f"请求失败，状态码：{response.status_code}")
def song_download():
    save_directory = "song_cover"
    df=pd.read_csv('song.csv',encoding='utf-8')
    cover=df['cover']
    name=df['name']
    song_id=df['song_id']
    for i in range(len(cover)):
        #if i==1018 or i==1760:
        try:
            download_image(cover[i], f"{save_directory}/{song_id[i]}.jpg")
        except Exception as e:
            print(f"歌曲下载失败!,第{i}个,名字{name[i]},cover:{cover[i]}")
            print(e) 
    print("歌曲封面下载完成！")

def singer_download():
    save_directory_2 = "singer_cover"
    df=pd.read_csv('singer.csv',encoding='utf-8')
    cover=df['cover']
    name=df['name']
    singer_id=df['singer_id']
    for i in range(len(cover)):
       # if i==315:
        try:
            download_image(cover[i], f"{save_directory_2}/{singer_id[i]}.jpg")
        except Exception as e:
            print(f"歌手下载失败!,第{i}个,名字{name[i]},cover:{cover[i]}")
            print(e)
    print("歌手封面下载完成！")
if __name__ == '__main__':
    song_download()
    singer_download()