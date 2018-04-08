import MySQLdb
# conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='ws940113ZYF',db='test',charset='utf8')
# cur=conn.cursor()
#
# cur.execute("""
# create table if not EXISTS account
# (
#   accid int(10) PRIMARY KEY ,
#   money int(10)
# )
# """)
#
# cur.execute('insert into account(accid,money) VALUES (1,110)')
# cur.execute('insert into account(accid,money) VALUES (2,10)')
#
# conn.commit()
# cur.close()
# conn.close()

import sys

class transfermoney(object):
    def __init__(self,conn):
        self.conn=conn
    def check(self,accid):
        cursor=self.conn.cursor()
        try:
            sql='select * from account where accid=%s'%accid
            cursor.execute(sql)
            print('check_acct_available' + sql)
            rs=cursor.fetchall()
            if len(rs)!=1:
                raise Exception('账号%s 不存在' %accid)
        finally:
            cursor.close()

    def enoughmoney(self,accid,money):
        cursor=self.conn.cursor()
        try:
            sql = 'select * from account where accid=%s and money>=%s' % (accid, money)
            cursor.execute(sql)
            print('reduce money'+sql)
            rs=cursor.fetchall()
            if len(rs)!=1:
                raise Exception('账号%s 减款失败' %accid)
        finally:
            cursor.close()

    def reducemoney(self,accid,money):
        cursor=self.conn.cursor()
        try:
            sql = 'update account set money=money-%s where accid=%s' % (money, accid)
            cursor.execute(sql)
            print('reduce money' + sql)
            rs = cursor.fetchall()
            if cursor.rowcount != 1:
                raise Exception('账号%s 减款失败' % accid)
        finally:
            cursor.close()

    def addmoney(self, accid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'update account set money=money+%s where accid=%s' % (money, accid)
            cursor.execute(sql)
            print('reduce money' + sql)
            rs = cursor.fetchall()
            if cursor.rowcount != 1:
                raise Exception('账号%s 加款失败' % accid)
        finally:
            cursor.close()

    def transfer(self,source_accid,target_accid,money):
        try:
            self.check(source_accid)
            self.check(target_accid)

            self.enoughmoney(source_accid,money)
            self.reducemoney(source_accid,money)
            self.addmoney(target_accid,money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()    #若出现异常，数据不发生变化
            raise e

if __name__=='__main__':
    source_accid=sys.argv[1]
    target_accid=sys.argv[2]
    money=sys.argv[3]

    conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='ws940113ZYF',db='test',charset='utf8')
    tr=transfermoney(conn)

    try:
        tr.transfer(source_accid,target_accid,money)
    except Exception as e:
        print('出现问题'+str(e))
    finally:
        conn.close()









