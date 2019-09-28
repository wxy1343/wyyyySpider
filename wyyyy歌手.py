import os

import  requests
from bs4 import BeautifulSoup
artist_id=input('请输入歌手id：')
url='https://music.163.com/artist?id='+artist_id
headers = {
    'referer': 'https://music.163.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
response=requests.get(url,headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
url = soup.find('ul', class_='f-hide').find_all('a')
artist_name=soup.find('h2', attrs={'data-rid':artist_id})['title']
print(artist_name)
for index,item in enumerate(url):
    song_id=item['href'].split('=')[-1]
    song_info = requests.get('https://music.163.com/api/song/detail/?ids=['+str(song_id)+']', headers=headers)
    song_name = song_info.json()['songs'][0]['name']
    song_artist = song_info.json()['songs'][0]['artists'][0]['name']
    print(song_name + '-' + song_artist)
    song = requests.get('https://music.163.com/song/media/outer/url?id=' + song_id, headers=headers, stream=True)
    try:
        song_lyric=requests.get('https://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1'.format(song_id),headers=headers).json()['lrc']['lyric']
    except:
        song_lyric = '纯音乐，无歌词'
    if (os.path.exists('music') != True):
        os.mkdir('music')
    if (os.path.exists(r'music/' + artist_name) != True):
        os.makedirs(r'music/' + artist_name)
    if (os.path.exists(r'./music/{}/{}-{}.mp3'.format(artist_name,song_name, song_artist))):
        continue
    with open(r'./music/{}/{}-{}.mp3'.format(artist_name,song_name, song_artist), 'wb') as f:
        for chunk in song.iter_content(chunk_size=128):
            f.write(chunk)
        with open(r'./music/{}/{}-{}.lrc'.format(artist_name,song_name, song_artist + '-' + song_artist), 'w', encoding='utf-8') as f:
            f.write(song_lyric)
    print('保存成功{}首'.format(index + 1))
