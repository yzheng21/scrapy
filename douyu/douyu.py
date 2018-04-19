# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
# driver = webdriver.PhantomJS(executable_path=r'C:\MyDrivers\phantomjs-2.1.1-windows\bin\phantomjs.exe')
# driver.get("http://www.qq.com")
# data = driver.title
# driver.save_screenshot('qq.png')
# print (data)


class Douyu():

    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path=r'C:\MyDrivers\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        self.num = 0
        self.count = 0

    def douyuspider(self):
        self.driver.get("https://www.douyu.com/directory/all")
        while True:
            soup = bs(self.driver.page_source,'lxml')
            names = soup.find_all("span",{'class':"dy-name ellipsis fl"})
            numbers = soup.find_all("span",{'class':"dy-num fr"})

            for name,number in zip(names,numbers):
                print(u"观众人数: -" + number.get_text().strip() + u"-\t房间名: " + name.get_text().strip())
                self.num += 1
                count = number.get_text().strip()
                if count[-1]=='万':
                    countNum = float(count[:-1])*10000
                else:
                    countNum = float(count)
                self.count += countNum

            self.driver.find_element_by_class_name("shark-pager-next").click()
            time.sleep(3)
            self.driver.implicitly_wait(3)
            if self.driver.page_source.find("shark-pager-disable-next") != -1:
                break

        print("当前网站直播人数:%s" % self.num)
        print("当前网站观众人数:%s" % self.count)

if __name__ == "__main__":
    d = Douyu()
    d.douyuspider()

