import re
def extra_Chinese(txt):
    pattern=re.compile("[\u4e00-\u9fa5]")
    return  "".join(pattern.findall(txt))# str.jion是链接字符串方法。
a=extra_Chinese("aaa任命。</p></p>3g资本成立与2222,")
print(a)