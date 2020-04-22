import requests
import re
import threading
import xlwt
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
    #except requests.RequestException:
    except Exception as e:
        print('无返回')
        return None

# 获取指定页面中含有guet.edu.cn的url
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



#都是一些全局变量
# 深度字典，{url：层级,...},用来去重，要控制层级所以要用字典，最终正确的去重数据在此
depthDict = {}
tmplist = []#临时存放url的队列
urlList = []#存已爬到的url
tlist=[]#加个线程列表
n=0
book=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=book.add_sheet('guetUrl',cell_overwrite_ok=True)
#              t=threading.Thread(target=getPageUrl(url))#之前的典型错误

##获取指定url中的所有url，并加入到待爬列表中，作为线程的target
def getSonPageUrl(url):#主体操作代码，去重存储都在这。
    try:
            subList = getPageUrl(url)
            for u in subList:
                if u not in depthDict:
                    depthDict[u] = depthDict[url] + 1
                    tmplist.append(u)
                    global n
                    #sheet.write(++n,0,u) #写入到excel里
                    # book.save('guetUrl.xls')#在这里存每次都刷新只能存下最近一个。3要全局变量，完成main后存，可以存所有的excel
                    #1往一个txt,doc里写url
                    #with open('dataMultiple.txt','a') as f:
                        #f.write('%d'%(n)+u+'\n')
                    #2把每个html写入文件
                    # html=getHtml(u)
                    # if html!=None:#过滤无效的空的html
                    #     try:#避免写空异常
                    #         n = n + 1
                    #         with open('./htmlMulti4Doc/%d.doc'%(n),'a',encoding='utf-8')as f2:
                    #             f2.write(html)
                    #     except Exception as e :
                    #         pass
                    print(u)

    except Exception as e:
        pass



def getUrls(depth):
    try:
        # 当还有待爬网页或者还有运行中的线程
        while ((len(tmplist) > 0) or (threading.activeCount() > 1)):
            while len(tmplist) == 0:
                continue#跳出本次循环
            url = tmplist.pop(0)
            if getHtml(url)==None:#过滤空的,在过滤html那里过滤后还需要这里。
                url = tmplist.pop(0)
                continue
            urlList.append(url)
            if depthDict[url]<depth:
                t=threading.Thread(target=getSonPageUrl,args=(url,))#格式要逗号,target要写对
                tlist.append(t)
                t.start()


    except Exception as e:
        pass

if __name__ == '__main__':
    startUrl = 'https://www.guet.edu.cn'
    # 爬取页面设置有第0级
    depthDict[startUrl] = 0
    tmplist.append(startUrl)
    getUrls(10)#获取目标网页的代码
    #book.save('guetUrl.xls')

#深度10层296个 广度5层283个