import jieba
import sqlite3

conn=sqlite3.connect('spider3.db')
cur=conn.cursor()
cursor=cur.execute("select content from GUET where id='8'")

for row in cursor:
    str=row[0]
print(str)
seg_list=jieba.cut(str)
print(" ".join(seg_list))
conn.close()