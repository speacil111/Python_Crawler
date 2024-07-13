import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
import re
import jieba
from collections import Counter

def conclusion1():
    song_count_by_singer = df_singer['song_num'].value_counts().sort_index()
    print(len(df_singer[df_singer['song_num']==1])/len(df_singer))
    print(len(df_singer[df_singer['song_num']==2])/len(df_singer))
    print(df_singer['song_num'].describe())
    #歌曲数量为1的歌手占比为0.73
    # 歌曲数量为2的歌手占比为0.14
    ax=song_count_by_singer.plot(kind='bar')
    plt.title('Number of Singers by Song Count')
    plt.xlabel('Number of Songs')
    plt.ylabel('Number of Singers')
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()
    top_5=df_singer.sort_values(by='song_num',ascending=False).head(5)
    #饼状图
    plt.figure(figsize=(8, 8))
    plt.pie(top_5['song_num'], labels=top_5['name'], autopct='%1.1f%%', startangle=140,textprops={'fontsize': 16})
    plt.title('Top 5 Singers by Song Count',fontsize=16)
    plt.show()

def conclusion2():
    #歌词词云图
    all_lyrics = ' '.join(df_song['lyric'].dropna())
    words_cut = jieba.cut(all_lyrics)
    words_spaced = ' '.join(words_cut)
    chinese_words = ' '.join(re.findall(r'[\u4e00-\u9fff]+', words_spaced))
    english_words = ' '.join(re.findall(r'[a-zA-Z]+', words_spaced))
    with open('cn_stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords_chinese = set([line.strip() for line in f.readlines()])
    stopwords_chinese_add = set([
    "暂时","歌词", "作词", "作曲","编曲","和声","制作人",
    "监制","想要","说","会","想","中","没一个","没有","里","走"
    ,"没","做","不会","一个","太","合","不能",' '])  
    stopwords_chinese.update(stopwords_chinese_add)
    stopwords_english = ['very', 'ourselves', 'am', 'doesn', 'through', 'me', 'against', 'up', 'just', 'her', 'ours', 
            'couldn', 'because', 'is', 'isn', 'it', 'only', 'in', 'such', 'too', 'mustn', 'under', 'their', 
            'if', 'to', 'my', 'himself', 'after', 'why', 'while', 'can', 'each', 'itself', 'his', 'all', 'once', 
            'herself', 'more', 'our', 'they', 'hasn', 'on', 'ma', 'them', 'its', 'where', 'did', 'll', 'you', 
            'didn', 'nor', 'as', 'now', 'before', 'those', 'yours', 'from', 'who', 'was', 'm', 'been', 'will', 
            'into', 'same', 'how', 'some', 'of', 'out', 'with', 's', 'being', 't', 'mightn', 'she', 'again', 'be', 
            'by', 'shan', 'have', 'yourselves', 'needn', 'and', 'are', 'o', 'these', 'further', 'most', 'yourself', 
            'having', 'aren', 'here', 'he', 'were', 'but', 'this', 'myself', 'own', 'we', 'so', 'i', 'does', 'both', 
            'when', 'between', 'd', 'had', 'the', 'y', 'has', 'down', 'off', 'than', 'haven', 'whom', 'wouldn', 
            'should', 've', 'over', 'themselves', 'few', 'then', 'hadn', 'what', 'until', 'won', 'no', 'about', 
            'any', 'that', 'for', 'shouldn', 'don', 'do', 'there', 'doing', 'an', 'or', 'ain', 'hers', 'wasn', 
            'weren', 'above', 'a', 'at', 'your', 'theirs', 'below', 'other', 'not', 're', 'him', 'during', 'which',
            'I','You',"I'm","You're","He","She","It","We","They","You'll"
            ,'And','oh','wanna','want','Oh','let','Let','yeah','Yeah','na','Na','la','La','ah','Ah',
            'go','Go','got','Got','get','Get','see','See','say','Say','come','Come','back','Back','take','Take',
            'But','one',]

    chinese_wordcloud = WordCloud(font_path='simhei.ttf', 
                                width=800, height=400, 
                                background_color='white',
                                stopwords=stopwords_chinese).generate(chinese_words)

    english_wordcloud = WordCloud(width=800, height=400, 
                                  background_color='white',
                                  stopwords=stopwords_english).generate(english_words)

    
    plt.figure(figsize=(10, 5))
    plt.imshow(chinese_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.figure(figsize=(10, 5))
    plt.imshow(english_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
#Top 5 热词
    chinese_words = jieba.cut(chinese_words)
    chinese_words_list = [word for word in chinese_words if word not in stopwords_chinese]
    english_words_list = [word for word in english_words.split() if word not in stopwords_english]
    total_chinese_words = len(chinese_words_list)
    total_english_words = len(english_words_list)
    chinese_words_counter = Counter(chinese_words_list)
    english_words_counter = Counter(english_words_list)
    top5_chinese_words = chinese_words_counter.most_common(5)
    top5_english_words = english_words_counter.most_common(5)

    for word, count in top5_chinese_words:
        proportion = count / total_chinese_words * 100
        print(f"{word}: {proportion:.2f}%")

    for word, count in top5_english_words:
        proportion = count / total_english_words * 100
        print(f"{word}: {proportion:.2f}%")

def conclusion3():
    chinese_songs = df_song[df_song['name'].apply(lambda x: bool(re.search(r'[\u4e00-\u9fff]', x)) and not re.search(r'[^\u4e00-\u9fff\s\(\)\[\]]', x))]
    #chinese_songs = df_song[df_song['name'].apply(lambda x: bool(re.search('[\u4e00-\u9fff]', x)))]
    chinese_songs['name_length'] = chinese_songs['name'].apply(lambda x: len(re.findall('[\u4e00-\u9fff]', x)))
    print(chinese_songs)
    char_pro=chinese_songs['name_length'].value_counts(normalize=True).sort_index()
    plt.figure(figsize=(10, 6))
    ax=char_pro.plot(kind='bar')
    plt.title('频率直方图',fontsize=16)
    plt.xlabel('歌名中汉字个数',fontsize=14)
    plt.ylabel('占比 (%)',fontsize=14)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10),
                  textcoords='offset points',fontsize=12)
    plt.show()
    print(chinese_songs[chinese_songs['name_length']==18]['name'])

    #画出歌名的词云图
    all_names = ' '.join(chinese_songs['name'])
    words_cut = jieba.cut(all_names)
    words_spaced = ' '.join(words_cut)
    chinese_words = ' '.join(re.findall(r'[\u4e00-\u9fff]+', words_spaced))
    with open('cn_stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords_chinese = set([line.strip() for line in f.readlines()])
    stopwords_chinese_add = set([
    "暂时","歌词", "作词", "作曲","编曲","和声","制作人",
    "监制","想要","说","会","想","中","没一个","没有","里","走"
    ,"没","做","不会","一个","太","合","不能",'爱',' '])  
    stopwords_chinese.update(stopwords_chinese_add)
    chinese_wordcloud = WordCloud(font_path='simhei.ttf', 
                                width=800, height=400, 
                                background_color='white',
                                stopwords=stopwords_chinese).generate(chinese_words)
    plt.figure(figsize=(10, 5))
    plt.imshow(chinese_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    chinese_words = jieba.cut(chinese_words)
    chinese_words_list = [word for word in chinese_words if word not in stopwords_chinese]
    total_chinese_words = len(chinese_words_list)
    chinese_words_counter = Counter(chinese_words_list)
    top5_chinese_words = chinese_words_counter.most_common(5)
    for word, count in top5_chinese_words:
        proportion = count / total_chinese_words * 100
        print(f"{word}: {proportion:.2f}%")
if __name__=='__main__':
    matplotlib.rcParams['font.family'] = 'SimHei'  #支持中文
    matplotlib.rcParams['axes.unicode_minus'] = False  

    df_song=pd.read_csv('song.csv')
    df_singer=pd.read_csv('singer.csv')
    df_singer['song_num']=df_singer['song_id'].apply(lambda x:len(x.split(',')))

    conclusion1()
    conclusion2()
    conclusion3()