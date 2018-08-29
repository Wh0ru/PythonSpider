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

def get_car():
    fc_options=Options()
    fc_options.add_argument('--headless')
    driver=webdriver.Chrome(chrome_options=fc_options)

    driver.get('http://product.auto.163.com/picture/#DQ2001')
    total_car=driver.find_elements_by_xpath(".//div[@class='brand_name']/h2//a")
    names=driver.find_elements_by_xpath(".//div[@class='brand_name']/h2")
    urls={}
    for i in names:
        name=i.get_attribute('title')
        urls[name]=[]

    for i,j in zip(total_car,urls):
        url=i.get_attribute('href')
        urls[j]=[url]
    driver.close()
    driver.quit()
    return urls

def get_car_img(url,root):
    # fc_options=Options()
    # fc_options.add_argument('--headless')
    driver=webdriver.Chrome()
    driver.get(url)

    # car_url=driver.find_elements_by_xpath(".//span[@class='car-type']/a[1]")
    car_url=driver.find_elements_by_xpath(".//a[@class='img']")
    img_urls=collections.defaultdict(set)
    time.sleep(2)
    for i in range(len(car_url)):
        # try:
        car_name=car_url[i].get_attribute('title')
        car_url[i].click()
        time.sleep(3)
        try:
            more=driver.find_element_by_xpath(".//span[@class='refresh-text']")
            more.click()
        except:
            driver.back()
            car_url = driver.find_elements_by_xpath(".//a[@class='img']")
            continue
        flag = False
        time.sleep(3)
        max_page=0
        while True:
            next=None
            try:
                next = driver.find_element_by_xpath(".//a[@class='page-link next']")
            except:
                flag=True
            len_page=len(driver.find_elements_by_xpath(".//a[@class='page-link next']"))
            if len_page>=max_page:
                max_page=len_page
            else:
                flag=True
            for j in driver.find_elements_by_xpath(".//li[@style='display: block;']//img"):
                img_url=j.get_attribute('src')
                img_urls[car_name].add(img_url)
            if flag:
                break
            # time.sleep(2)
            next.click()
        if not os.path.exists(root + '/' + car_name):
            os.makedirs(root + '/' + car_name)
            for ind, y in enumerate(img_urls[car_name]):
                # if not os.path.exists(root + '/' + car_name):
                #     os.makedirs(root + '/' + car_name)
                try:
                    down_img(root + '/' + car_name, ind, y, headers)
                except:
                    pass
        driver.back()
        car_url = driver.find_elements_by_xpath(".//a[@class='img']")
    driver.close()
    driver.quit()
        # except:
        #     pass

def down_img(root_path,ind,url,headers):
    img_path=root_path+'/{}.jpg'.format(ind)
    response=requests.get(url,headers=headers)
    with open(img_path,'ab+')as f:
        f.write(response.content)

urls=get_car()
if not os.path.exists('car/'):
    os.makedirs('car/')
for ind,i in enumerate(urls):
    if ind in [0,1,2,3,4,5,6,7,8,9,10,11,12]:
        continue
    get_car_img(urls[i][0],'car/'+i)
# get_car_img('http://product.auto.163.com/picture/brandindex/topicid=293M0008.html#tpkpp1','奥迪')