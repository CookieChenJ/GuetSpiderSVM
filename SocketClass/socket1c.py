import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#设置socket参数
s.connect(('127.0.0.1',8088))#填入地址和端口号
print('I am connecting the server!')
client_info=s.__str__().split('=')
print('The family and type are ',client_info[2][14:21],' and ', client_info[3][11:20] )
print('The address and port are ',client_info[6][0:-1])
xx='request server info'
s.send(xx.encode('utf-8'))
str1 = s.recv(1024)
for xx in['ABCDEF','abcdef','123456','#']:#发送四个字符串
  s.send(xx.encode('utf-8'))#发送
  str1 = s.recv(1024)#接收
  str2 = str(str1,encoding = 'utf-8')
  print('The original string is:',xx,'\tthe processed string is:',str2)
s.close()#关闭套接字