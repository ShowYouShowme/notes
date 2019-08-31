### 安装和基本用法

+ 安装
	1. pip3 install bs4 --proxy http://127.0.0.1:8090
	2. pip3 install lxml --proxy http://127.0.0.1:8090
+ 使用
	1. 基本功能
		+  格式化 *soup.prettify()*
		+  获取标签及标签里的内容
	2. 示例代码
	```python
	from bs4 import BeautifulSoup
	
	html_doc = """
	<html><head><title>The Dormouse's story</title></head>
	<body>
	<p class="title"><b>The Dormouse's story</b></p>
	
	<p class="story">Once upon a time there were three little sisters; and their names were
	<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
	<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>
	
	<p class="story">...</p>
	"""
	
	soup = BeautifulSoup(html_doc, "lxml")
	print(soup.prettify())#格式化
	
	print(soup.title)#获取title标签
	print(soup.title.string)#获取title标签里面的内容
	#找到所有的a标签
	print(soup.find_all("a"))
	```

### 使用爬虫爬取新闻网站

+ 下载网页源码至html文件里，也可以用***requests.get***获取网页源码
+ 源码
```python
from bs4 import BeautifulSoup

url = "https://www.infoq.cn/"
f = open("src.html","r",encoding="utf-8")
root_path = "https://www.infoq.cn/"
html = f.read()
soup = BeautifulSoup(html,"lxml")
title_hrefs = soup.find_all("div", class_="list-item image-position-right")
for title_href in title_hrefs:
    title = title_href.find("a",class_="com-article-title")
    print("标题：%s 链接:%s" %(title.string, root_path + title.get("href")))
```
### 获取图片链接并下载图片
```python
from bs4 import  BeautifulSoup
import requests
import os
import shutil

#1: 下载图片
#2: 实现翻页
#3: 利用多线程
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "close",
    "Cookie": "_gauges_unique_hour=1; _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1",
    "Referer": "http://www.infoq.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"
}

def download_img(url,path):
    response = requests.get(url,stream=True)
    if response.status_code == 200:
        with open(path,"wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
def download_all_img(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    for pic_href in soup.find_all("div", class_="container pc"):
        for pic in pic_href.find_all("img"):
            img_url = pic.get("src")
            pos = str(img_url).find('?')
            img_url = img_url[0:pos]
            # print(img_url)
            dir = os.path.abspath("./img")
            file_name = os.path.basename(img_url)
            img_path = os.path.join(dir,file_name)
            print("开始下载 %s" %img_url)
            download_img(img_url,img_path)


url = "http://www.cnu.cc/discoveryPage/hot-人像?page="
for i in range(1,6):
    print("第 %d 页" %i)
    download_all_img(url + str(i))
```

