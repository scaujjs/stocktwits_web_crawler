import urllib.request
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utils import *
import time
import os,shutil

import pickle
from lxml import etree
from lxml.etree import tostring

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"


browser=webdriver.Chrome()
browser.get("https://stocktwits.com/")





js_bottom = "var q=document.documentElement.scrollTop=10000"



## seed MichaelGLamothe
## login manually to bypass Chaptcha
login_flag=True
while(login_flag):
    time.sleep(1)
    s=input("ok?")
    if s.strip()=="ok":
        login_flag=False





def get_name(html):
    html = etree.HTML(html)


    names=[]
    print(len(html.xpath('//li[@class="st_2oVjETQ"]')))

    for x in html.xpath('//li[@class="st_2oVjETQ"]'):
        names.append(x.xpath("div/a/ul/li/span[1]/text()")[0])
    return names



def get_neighbor(name):

    browser.get("https://stocktwits.com/%s/following"%(name))
    time.sleep(1)
    browser.execute_script(js_bottom)
    time.sleep(1)
    source = browser.page_source

    followingnames=get_name(source)


    browser.get("https://stocktwits.com/%s/followers"%(name))
    time.sleep(1)
    browser.execute_script(js_bottom)
    time.sleep(1)
    source = browser.page_source
    followernames = get_name(source)

    return followingnames,followernames



seedname=["Stocks_Crypto_Alerts","famabvall","SmoothTraveler"]
while True:
    name_we_have = [x[:-4] for x in os.listdir("../socialNetwork") if not x.startswith(".")]
    search_name=""
    for name in seedname:
        if name in name_we_have:
            continue
        else:
            search_name=name
            break

    if search_name !="":
        print(search_name)
        try:
            followingnames, followernames = get_neighbor(search_name)
        except Exception as e:
            continue

        seedname.extend(followingnames)
        seedname.extend(followernames)

        f=open("../socialNetwork/%s.pkl"%(search_name),"wb")
        f.write(pickle.dumps({"name":search_name,"followings":followingnames,"followers":followernames}))
        f.close()
    else:
        break


## username angusjiang
## password T9ZcpFk?3S+-8p%
