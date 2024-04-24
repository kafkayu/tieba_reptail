from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from fake_useragent import UserAgent
from ToolFunction import Tool
from ToolFunction import save_list_to_txt ,load_list_from_txt
import re



def get_html(url):
    # 随机获取一个动态ua
    headers = {
        "User-Agent": UserAgent().random
    }
    # 发起请求
    request = Request(url, headers=headers)
    # urlopen()获取页面，类型是字节，需要用decode()解码，转换成str类型
    respose = urlopen(request)
    return respose.read()

def save_html(filename,html_bytes):
    with open(filename,"wb") as f:
        f.write(html_bytes)

def getIndexPage(page):
        #获取内容
        #page = self.getpage()
        pattern = re.compile('<a data-tid.*?href="([^"]*)"', re.S)
        items = re.findall(pattern, page.decode('GBK'))
        contents = []
        p = Tool()
        for item in items:
            content = p.replace(item)
            contents.append(content)
        return contents
def main():
    startnum = 1
    num = 3 #input the num of pages
    keyword = "离婚冷静期"

    base_url = "https://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%C0%EB%BB%E9%C0%E4%BE%B2%C6%DA&rn=10&un=&only_thread=1&sm=1&sd=&ed=&pn="
    rootPath = "../src/"
    htmlPath = rootPath+ "HtmlList/"
    PURLPath = rootPath+ "PostURLList/"

    for pn in range(startnum,int(num)):
        base_url+=str(pn)
        args = {
            "pn":pn,#*50
            "kw":keyword,
            "only_thread":1,
            "isnew" :1,
            "qw":keyword,
        }
        filename = "page_" + str(pn)+".html"
        args = urlencode(args)
        print("Downloading... "+filename)
        html_bytes = get_html(base_url.format(args))
        IndexPage = getIndexPage(html_bytes )
        save_list_to_txt(IndexPage, PURLPath+'list_data.txt')
        save_html(htmlPath+filename,html_bytes)

if __name__ == '__main__':
    main()
