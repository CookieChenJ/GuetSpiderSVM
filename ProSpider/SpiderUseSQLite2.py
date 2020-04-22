import requests
import re
import sqlite3
import jieba
# 链接的正则表达式，注意是在标签中的href属性里的才是真正的链接
PATTERN_URl = "<a.*href=\"(https?://.*guet.edu.cn.*?)[\"|\'].*"


# 获取网页源代码，注意使用requests时访问https会有SSL验证，需要在get方法时关闭验证
def getHtml(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        response = requests.get(url, headers=headers)  # 这一步的bug解决方法:https://tieba.baidu.com/p/6456215945?traceid=
        # 设置header的反爬很重要
        response.encoding = response.apparent_encoding  # 有时候出现乱码，这时候就是编码问题了
        if response.status_code == 200:  # 状态码
            return response.text
    except requests.RequestException:
        print('无返回')
        return None

# 有时还是会有警告
#import urllib3
#urllib3.disable_warnings()

# 获取指定页面中含有的url
def getPageUrl(url, html=None):
    if html == None:
        html = getHtml(url)
    uList = re.findall(PATTERN_URl, html)
    for item1 in uList:
        if re.match('.*?printer.*?',item1):
            uList.remove(item1)
        if re.match('.*?ipclient.*?',item1):
            uList.remove(item1)
        if re.match('.*?login.*?',item1):
            uList.remove(item1)
        if re.match('.*?pdf.*?', item1):
            uList.remove(item1)
    return uList


# 深度字典，{url：层级,...},用来去重，要控制层级所以要用字典#最终正确的去重数据在此
depthDict = {}
#临时存放url的列表，作为待爬列表，通过队列FIFO特性遍历url
tmplist = []
#存已爬到的url
urlList = []
n=0
#广度爬取

def extra_chinese(txt):
    pattern=re.compile("[\u4e00-\u9fa5]")
    return "".join(pattern.findall(txt))

def getUrls(depth):
    while (len(tmplist)>0):
        try:                                                        #避免要登录时候程序中断
            #从临时列表中移除并获取对首元素链接
            url = tmplist.pop(0)
            #添加到链接列表
            # if 'printer' in str(url):
            if getHtml(url)==None:#过滤返回为空的,
                url = tmplist.pop(0)
                continue
            urlList.append(url)
            if depthDict[url] < depth:
                # 获取子页面url列表

                subList = getPageUrl(url)
                for u in subList:
                    if u not in depthDict:#去重，通过与depthDict已有的比
                        depthDict[u] = depthDict[url] + 1
                        tmplist.append(u)#入队
                        print(u)

                        html=getHtml(u)
                        if html!=None:
                            try:
                                chinese=extra_chinese(html)
                                seg_list=jieba.cut(chinese)
                                JiebaChinese=" ".join(seg_list)
                                cur.execute("INSERT INTO JIEBA values(?,?,?)",(None,u,JiebaChinese))
                                conn.commit()
                            except Exception as e:
                                pass

        except Exception as e:
            print('需登录')
            pass


if __name__ == '__main__':
    conn=sqlite3.connect("spider3.db")
    cur=conn.cursor()
    startUrl = 'https://www.guet.edu.cn'
    # 爬取页面设置有第0级
    depthDict[startUrl] = 0
    tmplist.append(startUrl)
    getUrls(10)#获取目标网页的代码
    conn.close()


#深度10层296个 广度10层311个