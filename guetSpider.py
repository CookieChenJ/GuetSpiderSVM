import requests
import re

# 链接的正则表达式
PATTERN_URl = "<a.*href=\"(https?://.*guet.edu.cn.*?)[\"|\'].*"


# 获取网页源代码，
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

# 获取指定页面中含有guet.edu.cn的url
def getPageUrl(url, html=None):
    if html == None:
        html = getHtml(url)
    uList = re.findall(PATTERN_URl, html)
    return uList


# 深度字典，{url：层级,...},用来去重，要控制层级所以要用字典
depthDict = {}
n=0
#深度爬取
def getUrlsDeep(url, depth=10):
    try:
        if (depthDict[url] >= depth):
            return


        if 'printer'  in str(url):
            return
        if getHtml(url)==None:
            return
        if 'ipclient' in str(url):
            return
        # 获取此页中的所有连接
        clist = getPageUrl(url)
        # print("\t\t" * depthDict[url], "#%d:%s" % (depthDict[url], url))
        for c in clist:
            # 判断深度字典有有无此键，达到去重目的
            if c not in depthDict:  # 如果直接和depthDict比较，会发现item相同而层级不同时，也判断不重复。所以要比较item
                depthDict[c] = depthDict[url] + 1
                print('#%d' % depthDict[c], c)  # 打印过程


                with open('dataDeep2.txt', 'a') as f:  # 权限为all
                    f.write(c + '\n')
                # global n  # 定义全局txt文件编号
                # html = getHtml(c)  # 获取html的text
                # if html!=None:#空html不存
                #     try:  # 防止空写异常造成程序停止
                #         n = n + 1
                #         with open('./htmlDeep/%d.txt' % (n), 'a', encoding='utf-8')as f2:
                #             f2.write(html)
                #     except Exception as e:
                #         pass
                getUrlsDeep(c)


    except Exception as e:
        print('需登录')
        pass


if __name__ == '__main__':
    startUrl = 'https://www.guet.edu.cn'

    # 爬取页面设置有第0级
    depthDict[startUrl] = 0
    # 一共爬取depth级
    getUrlsDeep(startUrl, depth=10)
    #for value in depthDict.items():
        #print(value)
