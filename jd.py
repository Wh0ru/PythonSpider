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

def get_urls():
    fc_options=Options()
    fc_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=fc_options)
    driver.get('https://search.jd.com/search?keyword=%E6%91%A9%E6%89%98%E8%BD%A6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&uc=0#J_searchWrap')
    count=1
    urls = {}
    while True:
        total_bike_url=driver.find_elements_by_xpath(".//ul[@class='gl-warp clearfix']//div[@class='p-img']/a")
        for i in total_bike_url:
            name=i.get_attribute('title')
            url=i.get_attribute('href')
            urls[name]=url
        count+=1
        if count==8:
            break
        next=driver.find_element_by_xpath(".//a[@class='pn-next']")
        next.click()
        time.sleep(2)
    driver.close()
    driver.quit()
    return urls

def get_pic(url,root):
    fc_options=Options()
    fc_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=fc_options)
    driver.get(url)
    pic_urls=[]
    pics=driver.find_elements_by_xpath(".//ul[@class='lh']/li/img")
    for i in pics:
        pic_urls.append(i.get_attribute('src'))
    if not os.path.exists(root):
        os.makedirs(root)
    for ind,i in enumerate(pic_urls):
        i=i.split('n')
        j=i[1][1:]
        j='n1'+j
        i=i[0]+j
        down_img(root,ind,i,headers)
    driver.close()
    driver.quit()

def down_img(root_path,ind,url,headers):
    img_path=root_path+'/{}.jpg'.format(ind)
    response=requests.get(url,headers=headers)
    with open(img_path,'ab+')as f:
        f.write(response.content)

urls=get_urls()

if not os.path.exists('D:/jd_bike/'):
    os.makedirs('D:/jd_bike/')

for ind,i in enumerate(urls):
    get_pic(urls[i],'D:/jd_bike/'+str(ind))


# ".//ul[@class='lh']/li/img"