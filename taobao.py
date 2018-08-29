from selenium import webdriver
import threading
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import os
from selenium.webdriver.chrome.options import Options

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

key_word=input('keyword:')

if not os.path.exists(key_word):
    os.mkdir(key_word)

def down_img(root_path,ind,url,headers):
    img_path=root_path+'/{}.jpg'.format(ind)
    response=requests.get('http:'+url,headers=headers)
    with open(img_path,'ab+')as f:
        f.write(response.content)

fc_options=Options()
fc_options.add_argument('--headless')
driver=webdriver.Chrome(chrome_options=fc_options)
# driver=webdriver.PhantomJS()
driver.get('https://www.taobao.com/')

search=driver.find_element_by_class_name('search-combobox-input-wrap')
action_a=ActionChains(driver)
action_a.move_to_element(search).click().send_keys(key_word).send_keys(Keys.RETURN).perform()

driver.switch_to_window(driver.window_handles[-1])
time.sleep(2)
count=0
flag=False

while True:
    try:
        next=driver.find_element_by_css_selector("[class='item next next-disabled']")
        flag=True
    except:
        pass

    img_element=driver.find_elements_by_xpath(".//div[@class='item J_MouserOnverReq  ']//a/img")
    img_urls=[]
    threads=[]
    for i in img_element:
        img_url = i.get_attribute('data-src')
        img_urls.append(img_url)

    for ind,i in enumerate(img_urls):
        ind=ind+count
        f=threading.Thread(target=down_img,args=(key_word,ind,i,headers))
        threads.append(f)

    count += len(img_urls)

    for i in threads:
        i.start()
    if flag:
        break
    nt=driver.find_element_by_css_selector("[class='item next']")
    nt.click()
    driver.switch_to_window(driver.window_handles[-1])
    time.sleep(5)

driver.close()
driver.quit()

