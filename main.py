# coding:utf-8

import urllib
import urllib2
import cookielib
import re

def login():
    xn={}
    xn['email']=''
    xn['password']=''
    
    cookie=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    
    zhanghao = urllib.urlencode(xn)
    req=urllib2.Request('http://3g.renren.com/login.do?fx=0&autoLogin=true',zhanghao)
    html=urllib2.urlopen(req)
    
    return html.read()

def find_img_url(page):
#     match = re.findall(r'<title>(.*?)</title>', start_page, re.S)
    match = re.findall(r'&nbsp;<a href="(http://[^3].*?)">.*?</a>', page.decode("utf-8"), re.S)
#     if match != []:
    url = match[0]
#     else:
#         match = re.findall(r'<a href="(http://fmn.xnpic.com/.*?)">.*?</a>', page.decode("utf-8"), re.S)
#         url = match[0]
    return url

def find_page_num(page):
    match = re.findall(r'<span class="gray">\(.*?(\d+).*?\)</span>', page.decode("utf-8"), re.S)
    page_num = match[0]
    return page_num

def download(url,cur_page_num):
    urllib.urlretrieve(url,cur_page_num+'.jpg')
    
def find_next(page):
    match = re.findall(r'</p></div><div class="sec"><a href="(http://3g.renren.com/album/.*?)">.*?</a>', page.decode("utf-8"), re.S)
    next_url = match[0]
    return next_url

if __name__ == '__main__':
    login()

#     start_url shoule be the url of the first pic, not the url of the album
    start_url = ""
    start_page = urllib2.urlopen(start_url).read()
    str_page_num = find_page_num(start_page)
    
    int_page_num = int(str_page_num)
    cur_page = start_page
    while int_page_num !=  0:
        img_url = find_img_url(cur_page)
        download(img_url, str(int_page_num))
        next_url = find_next(cur_page)
        next_url = next_url.replace('&amp;','&')
        cur_page = urllib2.urlopen(next_url).read()
        int_page_num = int_page_num - 1
    print "Work Done !"
        