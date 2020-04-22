import requests
import re

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

# 有时还是会有警告，可以采用以下方式禁用警告
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
        if re.match('.*?ipclient.*?', item1):
            uList.remove(item1)
        if re.match('.*?login.*?', item1):
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
def getUrls(depth):
    while (len(tmplist)>0):
        try:                                                        #避免要登录时候程序中断
            #从临时列表中移除并获取对首元素链接
            url = tmplist.pop(0)
            #添加到链接列表
            urlList.append(url)
            if depthDict[url] < depth:
                # 获取子页面url列表
                subList = getPageUrl(url)
                for u in subList:
                    if u not in depthDict:#去重，通过与depthDict已有的比
                        depthDict[u] = depthDict[url] + 1
                        tmplist.append(u)#入队
                        print(u)
                        #with open('dataWide.txt','a') as f:#存url
                            #f.write(u+'\n')
                        html=getHtml(u)

                        # global n
                        # if html!=None:
                        #     try:#若写空会异常，所以要try
                        #         n = n + 1#非空才写才增
                        #         with open('./htmlWide/%d.txt'%(n),'a',encoding='utf-8') as f2:
                        #             f2.write(html)
                        #     except Exception as e :
                        #         pass

        except Exception as e:
            print('需登录')
            pass


if __name__ == '__main__':
    startUrl = 'https://www.guet.edu.cn'
    # 爬取页面设置有第0级
    depthDict[startUrl] = 0
    tmplist.append(startUrl)
    getUrls(5)#获取目标网页的代码
    #print('x2')
    #for url in urlList:
        #print(url)

#深度10层296个 广度5层283个