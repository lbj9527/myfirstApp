"""
一个HTML文件，找出里面的正文和链接和图片
"""
#request模块功能
#HTTP库
#支持HTTP连接保持和连接池，支持使用cookie保持会话，
#支持文件上传，支持自动响应内容的编码，支持国际化的URL和POST数据自动编码
import requests, re, os         
from bs4 import BeautifulSoup   #解析html

#例子1：获取网站正文
def getUrlBody():
    url = 'http://linyii.com'
    data = requests.get(url)
    r = re.findall(r'<body>[\s\S]*</body>', data.text)
    print(r[0])

    print('-------------------------------------------')
    soup = BeautifulSoup(data.text, 'html.parser')
    print(soup.body.text)

#例子2：获取网站链接
def getUrlLink():
    url = 'http://linyii.com'
    data = requests.get(url)

    soup = BeautifulSoup(data.text, 'html.parser')
    urls = soup.findAll('a')
    for u in urls:
        print(u['href'])

#例子3：获取百度贴吧美女图片
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

#例子4：获取虎扑步行街美女图片及视频
def getHupuUrl(startPage,stopPage,videoOrPic= False):
    #虎扑步行街主干道1-10页的帖子链接
    for index in range(startPage,stopPage):
        print('步行街主干道第%s页' % index)
        url = 'https://bbs.hupu.com/bxj'
        if index==1:
            url = url
        else:
            url = url + '-' + str(index)
        print(url)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        urls = soup.findAll('a', target="_blank")
        print(urls)
        for url in urls:
            srcs = url['href']
            words = re.findall(r'/[0-9]{8}\.html', srcs)
            for word in words:
                address = 'https://bbs.hupu.com' + word

                #只爬取每个帖子第一页
                if '-' in word:
                    continue
                
                #进入帖子
                if videoOrPic:
                    getOnePageVideo(address)
                else:
                    getOnePagePic(address)

#例子5：获取虎扑单个帖子图片
def getOnePagePic(img_address = str()):
     #进入帖子
    img_html = requests.get(img_address)
    soup_img = BeautifulSoup(img_html.text, 'html.parser')
    img_urls2 = soup_img.findAll('img')
 

    for img_url in img_urls2:

        img_src = img_url.get("src","none")
        if img_src == "none":
            continue

        img_src2 = img_url.get("data-original","none")
        if img_src2 != "none":
            img_src  = img_src2                     

        filename = os.path.split(img_src)[1]

        #url切片，提取真正的网址
        if filename == 'format,webp':
            img_src = img_src[0:(img_src.index('?'))]
            filename = os.path.split(img_src)[1]

        #以下图片格式不爬
        if filename[-3:] == 'png':
            continue

        if 'octet-stream' in filename:
            continue
            
        if filename in ['185','default_small.jpg']:
            continue

        if '?' in filename:
            continue
            
        if '.' in filename:
            print("图片链接：%s" % img_src)
            with open('pic/girls/' + filename, 'wb') as f:
                f.write(requests.get(img_src).content)    #下载图片

#例子4：获取虎扑单个帖子视频
def getOnePageVideo(video_address = str()):
     #进入帖子
    print("进入帖子")
    video_html = requests.get(video_address)
    soup_video = BeautifulSoup(video_html.text, 'html.parser')
    video_urls = soup_video.findAll('video')
 

    for video_url in video_urls:

        video_src = video_url.get("src","none")
        if video_src == "none":
            continue                   
        

        #url切片，提取真正的网址
        if 'mp4' in video_src:
            video_src_tmp = video_src[0:(video_src.index('?'))]
            filename = os.path.split(video_src_tmp)[1]

        else:
            return

        #以下格式不爬
        if '?' in filename:
            continue
            
        if '.' in filename:
            print("视频链接：%s" % video_src)
            with open('video/girls/' + filename, 'wb') as f:
                f.write(requests.get(video_src).content)    #下载视频



if __name__ == "__main__":
    #getUrlBody()
    #getUrlLink()
    #getTiebaPic()

    getHupuUrl(11,21,False)
    #getOnePageVideo('https://bbs.hupu.com/32131532.html')





##########################备注###########################
#1.运行getTiebaPic(),getOnePagePic()之前，在pic目录下创建girls/目录
#2.运行getOnePageVideo之前，在video目录下创建girls/目录


