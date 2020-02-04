"""
一个HTML文件，找出里面的正文和链接和图片，参考https://www.jianshu.com/p/257048bb4824
"""
#request模块功能
#HTTP库
#支持HTTP连接保持和连接池，支持使用cookie保持会话，
#支持文件上传，支持自动响应内容的编码，支持国际化的URL和POST数据自动编码
import requests, re, os , sys        
from bs4 import BeautifulSoup   #解析html
from fake_useragent import UserAgent
from pyquery import PyQuery as pq
import urllib


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
def getHupuUrl(keyword, startPage, stopPage, videoOrPic= False):
    #虎扑步行街主干道的帖子链接
    for index in range(startPage,stopPage):
        print('-----------------------------搜索%s关键词:第%d页-----------------------------' % (urllib.parse.unquote(keyword),index))

        url =  'https://my.hupu.com/search?q=' + keyword + '&sortby=createtime&page=' + str(index) + '&fid=&type=undefined'

        #虚拟一个headers：使用UserAgent伪造一个用户，添加自己的cookie
        ua = UserAgent()
        hs = {'user-agent':ua.random,'cookie':'_dacevid3=d45addeb.76df.8827.9ddb.d9b8bd3538d1; acw_tc=76b20f6a15807208550333511e6048812a60cd5e76a7e23e56f0a7a314412d; __gads=ID=f0266ab11f7a03e0:T=1580720857:S=ALNI_MagBH-J7WMb_uniATmi3TEKwQJLlg; _fmdata=4mpUKjarJLOffOtXKfD2vzb%2B7fsRpeT9lDmsk7w0WFvRJ02GrVRreTdzU15dep%2BtPh%2BdjVcouL0XJHmqajM1C57pwW4MrnoPLAKjbMezhI4%3D; _ga=GA1.2.884080577.1580754832; _gid=GA1.2.135845903.1580754832; __dacevid3=0xc0a0b535ad0a166d; __closeapp=1; _HUPUSSOID=50310739-338f-489f-bdd5-3a31fbf81361; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221700a4e53eb4f-08d457ee4c087b-b383f66-1440000-1700a4e53edfb%22%2C%22%24device_id%22%3A%221700a4e53eb4f-08d457ee4c087b-b383f66-1440000-1700a4e53edfb%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%7D; _cnzz_CV30020080=buzi_cookie%7Cd45addeb.76df.8827.9ddb.d9b8bd3538d1%7C-1; AUM=dg77BvbLBJirihebQtxZUlKnjN5nt-yqlWtWpTno5j7lw; _CLT=b0c2a05996d8b48b354e1fa4ddfc1fef; u=64110360|6JmO5omRSlIwODU0MTQ1NjM3|4986|f5c133ad45dda64a8365ac20542d4164|45dda64a8365ac20|aHVwdV9lODI3Y2E3M2RlZmVlZWJk; us=91f8e68654c24668122c2162a8418f8c5bebaf73785106d71eb6fcb9502aaec8622ab596e70b21576c370304fbc2309e3d9e3313a3f45ff2e05330686732a434; ua=25914162; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1580755509,1580755513,1580760867,1580764183; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1580764218; __dacevst=0c861d90.e7d6475f|1580766036014','referer': url, 'sec-fetch-mode':'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1'}
        html = requests.get(url, headers=hs)

        soup = BeautifulSoup(html.text, 'html.parser')
        urls = soup.findAll('a', target="_blank")

        #获取当页所有用户的帖子链接
        ok_urls = list()
        for url in urls:
            srcs = url['href']
            tmpList = re.findall(r'/[0-9]{8}\.html', srcs)
            if len(tmpList):
                ok_urls.append(tmpList[0])
                tmpList.clear()

        #进入帖子
        for ok_url in ok_urls:
            address = 'https://bbs.hupu.com' + ok_url
            
            #只爬取每个帖子第一页
            if '-' in ok_url:
                continue
            
            i = index * (ok_urls.index(ok_url)+1)
            print('--------第%s页第%s条链接--------' % (index, ok_urls.index(ok_url)+1)) 
            print("帖子链接：", address)
            if videoOrPic:
                getOnePageVideo(address,i)
            else:
                getOnePagePic(address)

#例子5：获取虎扑单个帖子图片
def getOnePagePic(img_address = str()):
     #进入帖子
    img_html = requests.get(img_address)
    soup_img = BeautifulSoup(img_html.text, 'html.parser')
    img_urls2 = soup_img.findAll('img')
    img_url_set = set(img_urls2)        #避免重复下载
 

    for img_url in img_url_set:

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
        isFilter = True
        itFil = True
        filters = ['png', 'octet-stream', '185', 'default_small.jpg', 'gif']
        for filter in filters:
            if filter in filename:
                itFil = False
            isFilter = isFilter and itFil

        if not isFilter:
            continue
            
        if '.' in filename:
            print("图片链接：%s" % img_src)
            with open('pic/girls/' + filename, 'wb') as f:
                f.write(requests.get(img_src).content)    #下载图片

#例子6：获取虎扑单个帖子视频
def getOnePageVideo(video_address,videoIndex):
     #进入帖子
    video_html = requests.get(video_address)
    soup_video = BeautifulSoup(video_html.text, 'html.parser')
    video_urls = soup_video.findAll('video')
    video_url_set = set(video_urls)

    #获取帖子标题
    title = soup_video.title.string
    title = title[:title.index('-')].replace(' ','').replace('\n', '').replace('\r', '').replace('?', '').replace('!', '')

    for video_url in video_url_set:

        video_src = video_url.get("src","none")
        if video_src == "none":
            continue                   
        
        #video重命名
        if 'mp4' in video_src:
            filename = str(videoIndex) + '-' + title + '.mp4'
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
    getHupuUrl(urllib.parse.quote('微胖'), 1, 25, True)
    #getOnePageVideo('https://bbs.hupu.com/32134074.html',7)







##########################备注###########################
#1.运行getTiebaPic(),getOnePagePic()之前，在pic目录下创建girls/目录
#2.运行getOnePageVideo之前，在video目录下创建girls/目录
#3.获取虎扑的内容必须虚拟一个headers，否则只能爬取前10页


