import MySQLdb

conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='ws940113ZYF',db='xiaoshuo',charset='utf8')
cur=conn.cursor()

class Sql:
    @classmethod
    def insert(cls,xs_name,xs_author,category,name_id):
        sql='insert into dd_name(xs_name,xs_author,category,name_id) values(%(xs_name)s,%(xs_author)s,%(category)s,%(name_id)s)'
        value={
            'xs_name':xs_name,
            'xs_author':xs_author,
            'category':category,
            'name_id':name_id
        }
        cur.execute(sql,value)
        conn.commit()

    @classmethod
    def select_name(cls,name_id):
        sql = 'select EXISTS(select 1 from dd_name where name_id=%(name_id)s)'
        value={'name_id':name_id}
        cur.execute(sql,value)
        return cur.fetchall()[0]