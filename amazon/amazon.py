# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os

init_web = 'https://www.amazon.com'
web = 'https://www.amazon.com/gp/product/B00EPM7T1M/'   #只需要修改这里的网址就可以了

urls = []
get_urls = requests.get(web)
soup = BeautifulSoup(get_urls.text,'lxml')
init_url = soup.find('a',class_='a-link-emphasis a-text-bold')['href']
get_review = requests.get(init_web+init_url)
soup = BeautifulSoup(get_review.text,'lxml')

#get maxpage
res = r'<a .*?>(.*?)</a>'
for i in (soup.find_all('li',class_='page-button')):
    for content in (i.find_all('a')):
        pageindex = re.findall(res,str(content),re.S|re.M)
maxpage = int(pageindex[0])

#获取所有的评价url
for i in range(1,maxpage+1):
    url = init_web+init_url+'&pageNumber={}'
    url = url.format(i)
    urls.append(url)

i = 0

with open('data.csv', 'w', encoding='utf-8') as f:
    f.write('评论标题,评分,评论人,评论时间,产品属性,是否verified purchase,评论内容，多少人点赞\n')

with open('data.csv', 'a', encoding='utf-8') as f:
    for url in urls:
        i += 1

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        tags = soup.find_all('div', attrs={'class': 'a-section review'})

        for tag in tags:
            title = tag.find('a', class_='a-size-base a-link-normal review-title a-color-base a-text-bold').get_text().replace(',','')
            star = tag.find('span', class_='a-icon-alt').get_text()[0]
            reviewer = tag.find('a', class_='a-size-base a-link-normal author').get_text()
            try:
                Verified = tag.find('span', class_='a-size-mini a-color-state a-text-bold').get_text()
                if Verified == 'Verified Purchase':
                    Verified = '有'
                else:
                    Verified = '否'
            except:
                Verified = '否'
            body = tag.find('span', class_='a-size-base review-text').get_text().replace(',','')
            try:
                attr = tag.find('a', class_='a-size-mini a-link-normal a-color-secondary').get_text().split()
                if len(attr) > 2:
                    attr = str(attr[0]) + str(attr[1]) + '  ' + 'color:' + str(attr[-1])
                else:
                    attr = str(attr[0]) + str(attr[1])
            except:
                attr = '0'
            try:
                review = tag.find('span', class_='review-votes').get_text().split()[0]
            except:
                review = '0'
            time = tag.find('span', class_='a-size-base a-color-secondary review-date').get_text().replace(',','').split()[1:]
            time = '/'.join(time[0:])
            print('{},{},{},{},{},{},{},{}\n'.format(title, star, reviewer, time, attr, Verified, body, review))
            f.write('{},{},{},{},{},{},{},{}\n'.format(title, star, reviewer, time, attr, Verified, body, review))

        print(i)

