import requests
from bs4 import BeautifulSoup
import xlwt


def request_guet(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        response = requests.get(url,headers=headers)#这一步的bug解决方法:https://tieba.baidu.com/p/6456215945?traceid=
        #设置header的反爬很重要
        response.encoding = response.apparent_encoding#有时候出现乱码，这时候就是编码问题了
        if response.status_code == 200:#状态码
            return response.text
    except requests.RequestException:
        print('erro')
        return None





def save_(soup):
    list = soup.find_all(class_='frontMenu')
    for item in list:
        #item_href=item.find(class_='li').text
        item_href=item.a.text
        print('x')
        print(item_href)

def main():
    url = 'https://www.guet.edu.cn'
    html = request_guet(url)#获得html
    soup = BeautifulSoup(html, 'lxml')#用beautifulSoup解析数据
    #print('x')
    save_(soup)#处理解析过的数据
    #print('x2')


if __name__ == '__main__':

    main()

