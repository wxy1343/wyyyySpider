import requests
url='https://music.163.com/song/media/outer/url'
song_id=input('请输入歌曲id：')
params={'id':song_id}
headers = {
    'referer': 'https://music.163.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
response=requests.get(url,headers=headers,params=params,stream=True)
url='https://music.163.com/api/song/detail/?ids=['+str(song_id)+']'
song_info=requests.get(url,headers=headers)
song_name=song_info.json()['songs'][0]['name']
song_artist=song_info.json()['songs'][0]['artists'][0]['name']
print(song_name+'-'+song_artist)
with open('{}-{}.mp3'.format(song_name,song_artist),'wb') as f:
    for chunk in response.iter_content(chunk_size=128):
        f.write(chunk)
print('下载成功')
