import MySQLdb
conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='ws940113ZYF',db='test',charset='utf8')
cur=conn.cursor()

cur.execute("""
create table if not EXISTS user
(
  userid int(11) PRIMARY KEY ,
  username VARCHAR(20)
)
""")
for i in range(1,10):
    cur.execute("insert into user(userid,username) values('%d','%s')" %(int(i),'name'+str(i)))

sql_insert = 'insert into user(userid,username) values(10,"name10")'
sql_update = 'update user set username="name91" where userid=9'
sql_delete = 'delete from user where userid=3'

cur.execute(sql_insert)
print(cur.rowcount)
cur.execute(sql_update)
print(cur.rowcount)
cur.execute(sql_delete)
print(cur.rowcount)

conn.commit()



# sql = 'select * from user'
# cur.execute(sql)

# print(cur.rowcount)
#
# rs = cur.fetchone()
# print(rs)
#
# rs = cur.fetchmany(9)
# print(rs)

# res=cur.fetchall()
# for row in res:
#     print('userid=%s,userna=%s' %row)

cur.close()
conn.close()
