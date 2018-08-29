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
    driver.get('http://detail.zol.com.cn/convenienttravel/')
    flag = False
    urls = {}
    while True:
        next=None
        bike_name=driver.find_elements_by_xpath(".//ul[@id='J_PicMode']//a/img")
        total_bike_url=driver.find_elements_by_xpath(".//ul[@id='J_PicMode']//a[@class='pic']")
        for i,j in zip(bike_name,total_bike_url):
            name=i.get_attribute('alt')
            url=j.get_attribute('href')
            urls[name]=url
        try:
            next=driver.find_element_by_xpath(".//a[@class='next']")
        except:
            flag=True
        if flag:
            break
        next.click()
        time.sleep(2)
    driver.close()
    driver.quit()
    return urls

def get_more(url):
    fc_options=Options()
    fc_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=fc_options)
    driver.get(url)
    try:
        more=driver.find_element_by_xpath(".//div[@class='section-header-link']/a[text()='更多图片']")
        more.click()
        driver.switch_to_window(driver.window_handles[-1])
        try:
            more_more=driver.find_element_by_xpath(".//h3[contains(text(),'整体外观图 ')]/preceding-sibling::a")
            _url=more_more.get_attribute('href')
            driver.close()
            driver.quit()
            return _url
        except:
            driver.close()
            driver.quit()
            return False
    except:
        driver.close()
        driver.quit()
        return None

# print(get_more('http://detail.zol.com.cn/Convenienttravel/index1166735.shtml'))

def get_pic2(url,root):
    if not os.path.exists(root):
        os.makedirs(root)
        # fc_options=Options()
        # fc_options.add_argument('--headless')
        driver = webdriver.Chrome()
        driver.get(url)
        try:
            more=driver.find_element_by_xpath(".//div[@class='section-header-link']/a[text()='更多图片']")
            more.click()
            driver.switch_to_window(driver.window_handles[-1])
            pic_urls = []
            try:
                pics = driver.find_elements_by_xpath(".//ul[@class='picture-list clearfix']/li/a/img")
                for i in pics:
                    pic_urls.append(i.get_attribute('src'))
                for ind, i in enumerate(pic_urls):
                    i = i.split('_')
                    j = i[1][6:]
                    i = i[0] + j
                    down_img(root, ind, i, headers)
                driver.close()
                driver.quit()
            except:
                driver.close()
                driver.quit()
        except:
            driver.close()
            driver.quit()


def get_pic(url,root):
    # fc_options=Options()
    # fc_options.add_argument('--headless')
    if not os.path.exists(root):
        os.makedirs(root)
        driver = webdriver.Chrome()
        driver.get(url)
        pic_urls=[]
        pics=driver.find_elements_by_xpath(".//ul[@class='picture-list clearfix']/li/a/img")
        for i in pics:
            pic_urls.append(i.get_attribute('src'))
        for ind,i in enumerate(pic_urls):
            i=i.split('_')
            j=i[1][6:]
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
if not os.path.exists('D:/bike/'):
    os.makedirs('D:/bike/')

for i in urls:
    url=get_more(urls[i])
    if url is None:
        continue
    if url is False:
        get_pic2(urls[i], 'D:/bike/' + i)
        continue
    get_pic(url,'D:/bike/'+i)