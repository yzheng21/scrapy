from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from config import *
import pymongo
from pyquery import PyQuery as pq
browser = webdriver.PhantomJS(executable_path=r'C:\MyDrivers\phantomjs-2.1.1-windows\bin\phantomjs',service_args=SERVICE_ARGS)
browser.set_window_size(1400,900)
wait = WebDriverWait(browser,10)
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def search():
    print('search.....')
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mq")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_PopSearch > div.sb-search > div > form > input[type="submit"]:nth-child(2)')))
        input.send_keys(search_item)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_product()
        return total.text
    except TimeoutError:
        return search()

def next_page(page_number):
    print('page.....')
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_product()
    except TimeoutError:
        next_page(page_number)

def get_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product ={
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price ').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('保存成功',result)
    except Exception:
        print('失败')

def main():
    try:
        total = search()
        total = int(re.compile(r'(\d+)').search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    finally:
        browser.close()

if __name__=='__main__':
    main()
