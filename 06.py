"""
一个HTML文件，找出里面的正文。
"""
#request模块功能
#HTTP库
#支持HTTP连接保持和连接池，支持使用cookie保持会话，
#支持文件上传，支持自动响应内容的编码，支持国际化的URL和POST数据自动编码
import requests, re          
from bs4 import BeautifulSoup   #解析html

url = 'http://linyii.com'
data = requests.get(url)
r = re.findall(r'<body>[\s\S]*</body>', data.text)
print(r[0])

print('-------------------------------------------')
soup = BeautifulSoup(data.text, 'html.parser')
print(soup.body.text)

