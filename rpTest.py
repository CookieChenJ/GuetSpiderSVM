import re
def is_valid_email(addr):
    #if re.match(r'[.+?]+@+(gmail|microsoft|example)\.com',addr):
    if re.match(r'(.+?)+@(gmail|microsoft)\.[com]', addr):#用或的时候用()括号 用[]变成在范围内选择了，然后|失效
        return True#用()来使用，在[]用+不对   (.+?)大于等于[a-zA-Z\.]
    else:
        return False

print(is_valid_email('someone@gmail.com'))
