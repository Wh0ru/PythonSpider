from selenium import webdriver
import threading
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import os
from selenium.webdriver.chrome.options import Options

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/5   37.36',
}
thread1=[]


def get_car_url():
    # fc_options=Options()
    # fc_options.add_argument('--headless')
    driver=webdriver.Chrome()
    driver.get('http://www.hx2car.com/quanguo/soa1')


    more=driver.find_element_by_class_name('more')
    more.click()

    car1_urls={}
    car_1=driver.find_elements_by_xpath(".//div[@class='brand alertBoxed']/ul[1]//li//div[@class='brand_r']//a")
    car2_urls={}
    car_2=driver.find_elements_by_xpath(".//div[@class='brand alertBoxed']/ul[2]//li//div[@class='brand_r']//a")
    for ind,i in enumerate(car_1):
        car1=i.get_attribute('href')
        name=i.text
        car1_urls[name]=[car1]

    for ind,i in enumerate(car_2):
        car2=i.get_attribute('href')
        name=i.text
        car2_urls[name]=[car2]
    car1_urls.update(car2_urls)
    driver.close()
    driver.quit()
    return car1_urls


url='http://www.hx2car.com/quanguo/aodi/soa1t26'
def get_car_dt(url,root):
    # fc_options=Options()
    # fc_options.add_argument('--headless')
    driver=webdriver.Chrome()
    driver.get(url)
    flag=False
    while True:
        try:
            next=driver.find_element_by_xpath(".//a[@class='num'][2]").get_attribute('href')
            if next is None:
                flag=True
        except:
            pass
        next_ele = driver.find_element_by_xpath(".//a[@class='num'][2]")
        cat_dt=driver.find_elements_by_xpath(".//img[@class='lazy']")
        time.sleep(3)
        pic_urls = {}
        for ind,i in enumerate(cat_dt):
            i.click()
            driver.switch_to_window(driver.window_handles[-1])
            count = len(driver.find_elements_by_id('pic_index'))
            name=driver.find_element_by_class_name('B_title').text
            for j in range(count):
                car_ele=driver.find_element_by_id('focusBigImg_{}'.format(j))
                if j==0:
                    pic_urls[name]=[car_ele.get_attribute('p_img')]
                else:
                    pic_urls[name].append(car_ele.get_attribute('p_img'))
            for ind,url in enumerate(pic_urls[name]):
                if not os.path.exists(root+'/'+name):
                    os.makedirs(root+'/'+name)
                    try:
                        down_img(root+'/'+name,ind,url,headers)
                    except:
                        pass
            time.sleep(5)
            driver.switch_to_window(driver.window_handles[0])
        if flag:
            break
        next_ele.click()
        time.sleep(5)
    driver.close()
    driver.quit()




def down_img(root_path,ind,url,headers):
    img_path=root_path+'/{}.jpg'.format(ind)
    response=requests.get(url,headers=headers)
    with open(img_path,'ab+')as f:
        f.write(response.content)


car_url=get_car_url()
# get_car_dt(url,'奥迪')

for i in car_url:
    if not os.path.exists(os.path.join('car',i)):
        os.makedirs(os.path.join('car',i))
    for j in car_url[i]:
        f=threading.Thread(target=get_car_dt,args=(j,os.path.join('car',i)))
        thread1.append(f)

for i in range(len(thread1)):
    if i%2==0:
        thread1[i].start()
        thread1[i+1].start()
        time.sleep(3600)





