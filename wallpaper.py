#-*-coding:utf-8-*-
import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from urllib import urlretrieve
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Linux系统用户名
username = 'andy'
#linux系统语言环境
lang = 'zh-cn'
pic_dir_name = '图片' if (lang=='zh-cn') else 'Pictures'

def getPageSource(url):
    r = requests.get(url)
    source = pq(r.text)
    return source

def renderJSPage(url):
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    cap["phantomjs.page.settings.loadImages"] = False
    cap["phantomjs.page.settings.userAgent"] = "faking it"
    browser = webdriver.PhantomJS(desired_capabilities=cap)
    browser.get(url)
    return browser.page_source

base_url = 'http://www.ivsky.com'
url = 'http://www.ivsky.com/bizhi/fengjing_1920x1080/'
print '进入第一层地址'
source = getPageSource(url)

link_objs = source('.ali div a')

for link_obj in link_objs:
    print '进入第二层地址'
    link = pq(link_obj).attr('href')
    source = getPageSource(base_url+link)
    link_objs = source('.pli div a')
    for link_obj in link_objs:
        print '进入第三层地址'
        link = pq(link_obj).attr('href')
        source = pq(renderJSPage(base_url+link))
        pic_path = pq(source('#downloadbtn')).attr('href')
        name = pic_path.split('/')[-1]
        print '获取高清图片地址'
        urlretrieve(pic_path, r'/home/%s/%s/%s.jpg'%(username, pic_dir_name, name))
