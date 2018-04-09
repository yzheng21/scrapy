from .mysql import Sql
from book.items import BookItem

class bookpipeline(object):

    def process(self,item,spider):
        if isinstance(item,BookItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0]==1:
                print("已经存在")
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                Sql.insert(xs_name,xs_author,category,name_id)
                print("开始有小说标题")