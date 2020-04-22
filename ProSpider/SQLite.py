import sqlite3
#创建表
conn=sqlite3.connect('spider3.db')
print('connect ok')
c=conn.cursor()
c.execute('''CREATE TABLE JIEBA
(ID INTEGER  PRIMARY KEY AUTOINCREMENT,
URL            TEXT NOT NULL,
CONTENT        TEXT )
''')
print('Table create successfully')
conn.commit()
conn.close()
#insert 数据
