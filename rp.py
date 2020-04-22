import re
#content = 'Xiaoshuaib has 100 bananas'
#res=re.match('Xi.*(\d+)\s.*s$',content)
#print(res.group(1))
a='C45Jva452C#1431254 Python|JavaScript'
r=re.findall('\d',a)#+ match  \d number
print(r)
r=re.findall('\d*',a)#+ match  0  or more \d
print(r)
r=re.findall('\d+',a)#+ match  1 or more
print(r)
#use . match any char
r=re.findall('\d+.',a)#more 1 any
print(r)
#use .* match any character
r=re.findall('.*',a)
print(r)
r=re.findall('....',a)
print(r)
r=re.findall('.*J',a)#匹配到最后一个J
print(r)
r=re.findall('.*?1',a)#加个问号 非贪婪，匹配到每一个1都停止一次。
print(r)

r=re.findall('[12]',a)
print(r)
r=re.findall('[12][234][125]',a)
print(r)
r=re.findall('[123456789]+',a)#相当于/d
print(r)

test='010-12345678'
if re.match(r'^\d{3}-\d{3,8}',test):#{3，8}表示了要3-8个数字3-8即可，不能少于3 不能多于8 345678个都可以
    print('ok')
else:
    print("failed")

m=re.match(r'^(\d{3})-(\d{3,8})$','010-12345')#注意细节 分组操作
print(m.group(1),m.group(2))

print(re.split(r'\s','a b  c'))
print(re.split(r'\s+','a b  c'))#可切分多个空格
print(re.split(r'[\s\,\;]+','a,b;c  d;;e'))#放在[]内就可以共同

