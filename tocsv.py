import pandas as pd
def new_singer():
    df=pd.read_csv('singer.csv')
    #添加singer——id列 type=str
    df['singer_id']=df['url'].str.extract(r'id=(\d+)')
    #根据singer_id列去重

    df.drop_duplicates(subset='singer_id',keep='first',inplace=True)
    print(len(df))
    df.to_csv('singer.csv',index=False,header=True,encoding='utf-8')
def new_song():
    df=pd.read_csv('song.csv')
    #去重
    df['song_id']=df['url'].str.extract(r'id=(\d+)')
    df.drop_duplicates(subset='song_id',keep='first',inplace=True)
    print(len(df))
    df.to_csv('song.csv',index=False,header=True,encoding='utf-8')
def add_web_song():
    df1=pd.read_csv('singer.csv')
    df2=pd.read_csv('song.csv')
    df1['singer_id']=df1['singer_id'].astype(str)
    df2['singer_id']=df2['singer_id'].astype(str)
    print(type(df1['singer_id'][0]))
    print(type(df2['singer_id'][0]))
    #对每一个singer_id，找到对应的歌曲id,并以列表添加至新的songid列中
    song_id = []  # 初始化song_id列表
    song_cover=[]
    song_name=[]
    for singer_id in df1['singer_id']:
        song_list = df2[df2['singer_id'] == singer_id]['song_id'].tolist()
        song_id.append(song_list)
        song_cover.append(df2[df2['singer_id'] == singer_id]['cover'].tolist())
        song_name.append(df2[df2['singer_id'] == singer_id]['name'].tolist())
    df1['song_id'] = song_id
    df1['song_cover']=song_cover
    df1['song_name']=song_name
    #把列表转换成字符串形式以，分隔
    df1['song_id']=df1['song_id'].apply(lambda x:','.join(map(str,x)))
    df1['song_cover']=df1['song_cover'].apply(lambda x:','.join(map(str,x)))
    df1['song_name']=df1['song_name'].apply(lambda x:','.join(map(str,x)))
    df1.to_csv('singer.csv',index=False,header=True,encoding='utf-8')
if __name__ == '__main__':
    new_song()
    new_singer()
    add_web_song()
    

    #现在又1663首，接着爬400首歌