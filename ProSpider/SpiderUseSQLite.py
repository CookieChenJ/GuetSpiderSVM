import requests
import re
import threading
import xlwt
import sqlite3
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
        #print('222')
        return uList



#都是一些全局变量
# 深度字典，{url：层级,...},用来去重，要控制层级所以要用字典，最终正确的去重数据在此
depthDict = {}
tmplist = []#临时存放url的队列
urlList = []#存已爬到的url
tlist=[]#加个线程列表
n=0

def extra_chinese(txt):#提取中文
    pattern=re.compile("[\u4e00-\u9fa5]")
    return "".join(pattern.findall(txt))

def getSonPageUrl(url):#主体操作代码，去重存储都在这。
    # try:
            subList = getPageUrl(url)
            for u in subList:
                if u not in depthDict:#去重
                    depthDict[u] = depthDict[url] + 1
                    tmplist.append(u)
                    global n


                    #2把每个html写入到txt或者doc中
                    html=getHtml(u)
                    if html!=None:#过滤无效的空的html
                        # try:#避免写空异常
                            # 1往一个txt,doc里写url

                            cur.execute("INSERT INTO GUET values(?,?,?)",(None,u,chinese))
                            con.commit()
                            print('bb')
                            # n = n + 1
                            # with open('./htmlChinese/%d.txt'%(n),'a',encoding='utf-8')as f2:
                            #     f2.write(chinese)
                        # except Exception as e :
                        #     pass
                    print(u)

    # except Exception as e:
    #     print("cc")
    #     pass



def getUrls(depth):
    try:
        # 当还有待爬网页或者还有运行中的线程
        while ((len(tmplist) > 0) or (threading.activeCount() > 1)):
            while len(tmplist) == 0:
                continue#跳出本次循环
            url = tmplist.pop(0)
            if 'printer' in str(url):#过滤打印机
                continue
            if 'ipclient' in str(url):
                continue
            if getHtml(url)==None:#过滤空的
                continue
            urlList.append(url)
            if depthDict[url]<depth:
                t=threading.Thread(target=getSonPageUrl,args=(url,))#格式要逗号,target要写对
                tlist.append(t)
                t.start()
                #print('1111')

    except Exception as e:
        pass

    # def initDB(self, file_path):
    #     self.file_path = file_path
    #     self.cx = sqlite3.connect(file_path, check_same_thread=False)
    #     self.cx.execute(self.create_table_str)
    #     self.cx.execute(self.create_detail_table_str)
    #     print("init the table strucutre successfully")

if __name__ == '__main__':

    con=sqlite3.connect('spider.db')#链接数据库

    cur=con.cursor()#创建游标
    startUrl = 'https://www.guet.edu.cn'
    # 爬取页面设置有第0级
    depthDict[startUrl] = 0
    tmplist.append(startUrl)
    getUrls(5)#获取目标网页的代码
    con.close()


#深度10层296个 广度5层283个