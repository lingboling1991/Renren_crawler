#coding:utf-8
import urllib
import urllib2
import cookielib
import re
import os

def login():
    xn={}
    xn['email']='lingboling1991@yeah.net'
    xn['password']='123456'
    
#     xn={}
#     xn['email']='lingboling1991@126.com'
#     xn['password']='lcw@bupt'
    
    cookie=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    
    zhanghao = urllib.urlencode(xn)
    req=urllib2.Request('http://3g.renren.com/login.do?fx=0&autoLogin=true',zhanghao)
    html=urllib2.urlopen(req)
    
    return html.read()

def find_img_url(page):
    match = re.findall(r'&nbsp;<a href="(http://[^3].*?)">.*?</a>', page.decode("utf-8"), re.S)
    url = match[0]
    return url

def find_page_num(page):
    match = re.findall(r'<span class="gray">\(.*?(\d+).*?\)</span>', page.decode("utf-8"), re.S)
    page_num = match[0]
    return page_num

def download(url,str_page_num):
    ablum_name = get_ablum_name(start_page)
    urllib.urlretrieve(url,ablum_name + "/" + str_page_num+'.jpg')
    
def find_next(page):
    match = re.findall(r'</p></div><div class="sec"><a href="(http://3g.renren.com/album/.*?)">.*?</a>', page.decode("utf-8"), re.S)
    next_url = match[0]
    return next_url

def get_name(page,int_page_num):
    ablum_name = get_ablum_name(start_page)
    f = open(ablum_name + "/" + "BeiZhu"+'.txt','a')
    match = re.findall(r'<img src=".*?" align="" alt=".*?" class=""/></a><p>(.*?)<br />', page.decode("utf-8"), re.S)
    name = match[0]
    temp = re.findall(r'<a href=.*?', name, re.S)
    if(temp != []):
        name = ""
    else:
        name = name.encode('utf-8')
        f.write(str(int_page_num) + " " + name + "\n\n")
    f.close()
    
def get_ablum_name(page):
    match = re.findall(r'<div class="sec"><b>(.*?)</b>&nbsp;', page.decode("utf-8"), re.S)
    ablum_name = match[0]
    return ablum_name

if __name__ == '__main__':
    login()

#     start_url should be the url of the first pic, not the url of the album
    start_url = "http://3g.renren.com/album/wgetphoto.do?id=5784151942&albumid=356934022&owner=316312841&ret=profile.do%3Fid%3D316312841-n-%E8%87%A7%E4%BA%9A%E5%BC%BA%E7%9A%84%E4%B8%AA%E4%BA%BA%E4%B8%BB%E9%A1%B5-n-0-u-album%2Fwmyalbum.do%3Fid%3D316312841%26amp%3Bhtf%3D38-n-%E8%87%A7%E4%BA%9A%E5%BC%BA%E7%9A%84%E7%9B%B8%E5%86%8C-n-0-u-album%2Fwmyalbum.do%3Fcurpage%3D1%26amp%3Bid%3D316312841-n-%E8%87%A7%E4%BA%9A%E5%BC%BA%E7%9A%84%E7%9B%B8%E5%86%8C-n-0-u-album%2Fwgetalbum.do%3Fid%3D356934022%26owner%3D316312841-n-%E8%AF%A5%E7%9B%B8%E5%86%8C-n-0&sid=JBAEKOc0Ez4rR_udAYOa2Y&d4a5vo"
    start_page = urllib2.urlopen(start_url).read()
#     print start_page
    str_page_num = find_page_num(start_page)
    
    int_page_num = int(str_page_num)
    cur_page = start_page
    
    ablum_name = get_ablum_name(start_page)
    os.mkdir(ablum_name)
    
    while int_page_num !=  0:
        img_url = find_img_url(cur_page)
        download(img_url, str(int_page_num))
        get_name(cur_page,int_page_num)
        next_url = find_next(cur_page)
        next_url = next_url.replace('&amp;','&')
        cur_page = urllib2.urlopen(next_url).read()
        int_page_num = int_page_num - 1
    print "Work Done !"
        