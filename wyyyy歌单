import requests
import os
from bs4 import BeautifulSoup

headers = {
    'referer': 'https://music.163.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
url = 'https://music.163.com/playlist?id='
if __name__ == '__main__':
    song_list_id=input('请输入歌单id：')
    url= url + song_list_id
    response = requests.Session()
    response.headers = headers
    response = response.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    url = soup.find('ul', class_='f-hide').find_all('a')
    song_id = []
    song_name = []
    song_url = []
    song_artist = []
    song_info_name = []
    song_lyric_url=[]
    if (os.path.exists('music') != True):
        os.mkdir('music')
    if (os.path.exists(r'music/' + song_list_id) != True):
        os.makedirs(r'music/' + song_list_id)
    for index, item in enumerate(url):
        song_id.append(item['href'].split('=')[-1])
        song_url.append(r'https://music.163.com/song/media/outer/url?id=' + song_id[index])
        song_info_url = r'https://music.163.com/api/song/detail/?ids=[{}]'.format(song_id[index])
        song_info = requests.get(song_info_url,headers=headers)
        song_name.append(song_info.json()['songs'][0]['name'])
        song_artist.append(song_info.json()['songs'][0]['artists'][0]['name'])
        song_info_name.append(song_name[index] + '-' + song_artist[index])
        song_lyric_url.append('https://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1'.format(song_id[index]))
        try:
            song_lyric=requests.get(song_lyric_url[index],headers=headers).json()['lrc']['lyric']
        except:
            song_lyric='纯音乐，无歌词'
        print(index+1, '.', song_info_name[index], song_url[index])
        if (os.path.exists(r'./music/{}/{}.mp3'.format(song_list_id, song_info_name[index]))):
            continue
        song = requests.get(song_url[index], stream=True,headers=headers)
        with open(r'./music/{}/{}.mp3'.format(song_list_id, song_info_name[index]), 'wb') as f:
            for chunk in song.iter_content(chunk_size=128):
                f.write(chunk)
            with open(r'./music/{}/{}.lrc'.format(song_list_id, song_info_name[index]), 'w', encoding='utf-8') as f:
                f.write(song_lyric)
            print('保存成功{}首'.format(index + 1))
