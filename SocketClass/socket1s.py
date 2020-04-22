import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建并设置socket参数
s.bind(('127.0.0.1',8088))##设置地址和端口
s.listen(5)#监听
print('Wait for connecting…')
(conn,addr) = s.accept()#接受套接字
print('conn=',conn)
print('addr=',addr)

while True:
  str1 = conn.recv(1024)#接收数据
  str2 = str(str1,encoding = 'utf-8')
  print('I received a string is:',str2)
  if (str2.isupper()):
   str3 ='大写字母'
  elif (str2.islower()):
   str3 = '小写字母'
  elif (str2.isnumeric()):
   str3 = '数字'
  else:
   str3 = '结束命令'
  conn.send(str3.encode('utf-8'))#发送数据相应给客户端
  if str2 == '#': #结束标志
   break
conn.close()
s.close#关闭套接字