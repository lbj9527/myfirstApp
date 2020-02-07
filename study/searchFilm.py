import requests, re, os , sys        
from bs4 import BeautifulSoup   #解析html
from fake_useragent import UserAgent
import urllib
import multiprocessing
import time
import datetime


#获取苹果资源网链接
def getAppleUrl(startPage, stopPage):
    ok_urls = []
    for index in range(startPage,stopPage):
        print('-----------------------------进程:%s 开始爬取第%d页-----------------------------' % (os.getpid(), index))

        url =  'http://www.nx607.com/?m=vod-index-pg-' + str(index) + '.html'


        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        urls = soup.findAll('a', target="_blank")
        urls_set = set(urls)

        #获取当页所有视频的链接
        for url in urls_set:
            srcs = url['href']
            if 'vod-play' in srcs:
                ok_urls.append(srcs)
    return ok_urls

#获取m3u8一级网址
def getFirstUrl(srcurl):
        realurl = 'http://www.nx607.com' + srcurl
        html = requests.get(realurl)
        soup = BeautifulSoup(html.text, 'html.parser')
        results = soup.findAll('script')
        #print(results)
        for res in results:     
            if 'mac_url' in str(res):
                s = re.findall(r"https(.*).m3u8",str(res))
                return "https" + urllib.parse.unquote(s[0]) + ".m3u8"

#获取m3u8二级网址
def getSecondUrl(firsturl):
    return firsturl.replace('index.m3u8','550kb/hls/index.m3u8',1)

#获取m3u8切片网址
def getTsUrl(secondurl):
    content = requests.get(secondurl).text
    file_lines = content.split("\n")
    tsList = []
    for file_line in file_lines:
        if file_line[-2:] == 'ts':    
            tsList.append(secondurl.replace('index.m3u8', file_line,1))
    return tsList


def downOneVideo(firstUrl):
    download_path = os.getcwd() + r"\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        
    #新建日期文件夹
    download_path = os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    #print download_path
    os.mkdir(download_path)

    num = 0
    tsList = getTsUrl(getSecondUrl(firstUrl))
      
    with open(os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.ts'), 'ab') as f:
        for tsurl in tsList:
            num += 1
            print('----------------第%d段视频开始下载-------------------' % num)
            res = requests.get(tsurl)
            f.write(res.content)
            f.flush()

#待测试
def downloadVideoByIndex(srcpath, start, stop):
    download_path = os.getcwd() + r"\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        
    #新建日期文件夹
    download_path = os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    #print download_path
    os.mkdir(download_path)

    with open(srcpath, 'r') as f:
        urls = f.readlines()
        with open(os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.ts'), 'ab') as f:
            for i in urls:
                print('----------------第%d段视频开始下载-------------------')
                res = requests.get(i)
                #print(urls[i])
                f.write(res.content)
                f.flush()



       

if __name__ == "__main__": 

    #爬取链接
    # count = (13-1)*20
    # list = getAppleUrl(13 ,20)
    # for item in list:
    #     count += 1
    #     print('----第%d部电影地址开始下载----' % count)
    #     urls = getTsUrl(getSecondUrl(getFirstUrl(item)))
    #     with open(os.getcwd() + '/file/filmUrl/tsUrl-' + str(count) + '.txt', 'a') as f:
    #         rate = 0
    #         for tsurl in urls:
    #             rate += 1
    #             f.write(tsurl + '\n')
    #             print('%d / %d' % (rate, len(urls)))
    #         rate=0

    
    #从链接文件中，根据起止序号下载ts文件(待测试)
    #downloadVideoByIndex('file/filmUrl/tsUrl-45.txt',0,2)

                

    #print(getFirstUrl('/?m=vod-play-id-73801-src-1-num-1.html')) 
    #print(getSecondUrl('https://cdn3.lajiao-bo.com/20200108/0xqppjHO/index.m3u8'))
    #print(getTsUrl(getSecondUrl('https://cdn3.lajiao-bo.com/20200108/0xqppjHO/index.m3u8')))
    downOneVideo('https://cdn3.lajiao-bo.com/20191223/x46aAMhr/index.m3u8')