#! -*- encoding:utf-8 -*-\
from Mylog import MyLog
import string
from urllib.parse import quote
from urllib import error
import urllib.request
from bs4 import BeautifulSoup
import  codecs


class Item(object):
    title=None
    author=None
    lastreplypeople = None
    lastreplytime=None

class GetBaiTieBa(object):
    def __init__(self,url):
        self.url=url
        self.log=MyLog()
        self.pageSum=1#要爬取的页数
        self.urls=self.getUrls(self.pageSum) #根据pageSum拼装要爬取的地址
       #开始爬取
        self.items=self.spider(self.urls)
        #存
        self.pipelines(self.items)


    # 根据pageSum拼装要爬取的地址   思考一 ：如何确定总共有多少页数？
    def getUrls(self,pageSum):
        urls=[]
        pns=[ str(i*50) for i in range(pageSum)]
        ul=self.url.split('=')
        for pn in pns:
            ul[-1]=pn   #取最后一个'=' 也就是页数对应的数值  替换页数 0 50 100 150 200
            url='='.join( ul )
            urls.append( url )
            self.log.debug('----待爬取的地址有:'+url)
        self.log.info(u'获取URL成功')
        return urls

    #数据爬取 利用lxml解析
    def spider(self,urls):
        items=[]
        for url in urls:
            htmlContent=self.getResponseContent(url)
            soup=BeautifulSoup(htmlContent,'lxml')
            tagsli=soup.find_all('li',attrs={'class':' j_thread_list clearfix'})
            for tag in tagsli:
                item=Item()
                item.title=tag.find('a',attrs={'class':'j_th_tit '}).get_text().strip()
                item.author=tag.find('div',attrs={'class':'threadlist_author pull_right'}).span['title']
                #item.author = tag.find('span', attrs={'class': 'tb_icon_author '}).get('title') 错误
                item.lastreplypeople= tag.find('span', attrs={'class': 'tb_icon_author_rely j_replyer'})['title']
                item.lastreplytime=tag.find('span', attrs={'class': 'threadlist_reply_date pull_right j_reply_data'}).getText().strip()

                items.append(item)
                #self.log.info(u'获取标题为 -->%s--< 的帖子成功 作者是:%s' %(item.title,item.author))
                self.log.info(u'获取标题为 -->%s--< 的帖子成功' % (item.title))
        return items

    def getResponseContent(self,url):
        #对地址的中文进行编码
        try:
            url=quote(url,safe=string.printable)
            response=urllib.request.urlopen(url)
        except  error.URLError as e:
            self.log.error(u'python爬取%s 出错了' %url)
            print (e)
        else:
            self.log.info(u'python爬取%s 成功' %url)
            return response.read()

    # 保存爬取的文件
    def pipelines(self,items):
        fileName=u'tiebarizhi.txt'.encode('utf8')
        with codecs.open(fileName,'w','utf8') as fp:
            for item in items:
                fp.write('%s %s %s %s\t\t  \r\n' %(item.title,item.author,item.lastreplypeople,item.lastreplytime))
                #fp.write('%s \r\n' % (item.title))
                self.log.info(u'标题为 -->%s<-- 的帖子保存成功' %(item.title))

if __name__=='__main__':
    url=u'http://tieba.baidu.com/f?kw=权利的游戏&ie=utf-8&pn=50'
    print ('url:',url)
    tb=GetBaiTieBa(url)