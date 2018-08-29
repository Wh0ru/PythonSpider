from selenium import webdriver
import threading
import time
import collections
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import os
from selenium.webdriver.chrome.options import Options

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/5   37.36',
}

def get_urls(root):
    fc_options=Options()
    fc_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=fc_options)
    driver.get('http://product.mtuo.com/prolist-c1p0v0n0s0o0_1.html')
    flag = False
    while True:
        urls = {}
        next=None
        bike_name=driver.find_elements_by_xpath(".//td[@class='lan']/a[2]")
        img_url=driver.find_elements_by_xpath(".//td[@bgcolor='#FFFFFF']/a/img")
        for i,j in zip(bike_name,img_url):
            name=i.text
            url=j.get_attribute('src')
            urls[name]=url
            if not os.path.exists(root+name):
                os.makedirs(root+name)
        for ind,i in enumerate(urls):
            try:
                down_img(root+i,ind,urls[i],headers)
            except:
                pass
        try:
            next=driver.find_element_by_xpath(".//a[contains(text(),'下一页')]")
        except:
            flag=True
        if flag:
            break
        next.click()
        time.sleep(3)
    driver.close()
    driver.quit()
    return urls

def down_img(root_path,ind,url,headers):
    img_path=root_path+'/{}.jpg'.format(ind)
    response=requests.get(url,headers=headers)
    with open(img_path,'ab+')as f:
        f.write(response.content)

if not os.path.exists('D:/motu/'):
    os.makedirs('D:/motu/')
urls=get_urls('D:/motu/')
