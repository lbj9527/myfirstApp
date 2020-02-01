"""
一个HTML文件，找出里面的正文和链接和图片
"""
#request模块功能
#HTTP库
#支持HTTP连接保持和连接池，支持使用cookie保持会话，
#支持文件上传，支持自动响应内容的编码，支持国际化的URL和POST数据自动编码
import requests, re, os         
from bs4 import BeautifulSoup   #解析html

def getUrlBody():
    url = 'http://linyii.com'
    data = requests.get(url)
    r = re.findall(r'<body>[\s\S]*</body>', data.text)
    print(r[0])

    print('-------------------------------------------')
    soup = BeautifulSoup(data.text, 'html.parser')
    print(soup.body.text)

def getUrlLink():
    url = 'http://linyii.com'
    data = requests.get(url)

    soup = BeautifulSoup(data.text, 'html.parser')
    urls = soup.findAll('a')
    for u in urls:
        print(u['href'])

def getTiebaPic():
    url='http://tieba.baidu.com/p/2166231880'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    img_urls = soup.findAll('img',bdwater='杉本有美吧,1280,860')    #根据两个匹配条件,匹配出符合要求的html
    for img_url in img_urls:
        print(img_url)
        img_src = img_url['src']    #根据key(src)找出value
        print(img_src)
        with open('pic/girls/' + os.path.split(img_src)[1], 'wb') as f:
            f.write(requests.get(img_src).content)    #下载图片

if __name__ == "__main__":
    #getUrlBody()
    #getUrlLink()
    getTiebaPic()




##########################备注###########################
#1.运行getTiebaPic()之前，在pic目录下创建girl/目录


