import requests
import base64
from Crypto.Cipher import AES


second_param = '010001'
third_param = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
fourth_param = '0CoJUm6Qyw8W8jud'


def get_params():
    # 根据该加密算法做出解密
    iv = '0102030405060708'
    first_key = fourth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSeckey():
    # 这个也是定值
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    if type(text) == type(b'123'):
        # 这是判断当前变量的类型是bytes还是字符串，因为pycryptodome要
        # 求参数要是字节类型
        text = text.decode('utf-8')

    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)

    iv = iv.encode('utf-8')
    key = key.encode('utf-8')
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    text = text.encode('utf-8')
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


song_id = input('请输入歌曲id：')
first_param = '{rid: "R_SO_4_%s", offset: "120", total: "true", limit: "100", csrf_token: ""}'%(song_id)# 第一页时为true，其他页为false
params = get_params()
encSecKey = get_encSeckey()
data = {'params': params, 'encSecKey': encSecKey}
headers = {
    'referer': 'https://music.163.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)
req = requests.post(url, headers=headers, data=data)
for i in req.json()['comments']:
    name=i['user']['nickname']
    content=i['content']
    print('*'*10)
    print(name+':'+content)
print('*'*10)
