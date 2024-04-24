import urllib
import urllib.request
import re
import csv
import emojiswitch
def save_list_to_txt(data, filename):
    with open(filename, 'a') as file:
        for item in data:
            file.write(str(item) + '\n')

def load_list_from_txt(filename):
    with open(filename, 'r') as file:
        data = file.read().splitlines()
    return data
class Tool:
    #替换工具
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()
class BDTB:

    def __init__(self, baseUrl, seeLZ, floorTag):
        #初始化输入
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.files = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getpage(self, pageNum):
        #获取贴吧页面
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            #print response.read()

            return response.read()

        except urllib.error.URLError as e:
            if hasattr(e, "reason"):

                print("连接百度贴吧失败，错误原因", e.reason)
    def getFname(self,page):

        pattern = re.compile('<a class="card_title_fname.*?>(.*?)</a>', re.S)
        result = re.search(pattern, page.decode('utf-8'))
        if result:
            return result.group(1).strip()
        else:
            return None


    def getTitle(self, page):
        #获取标题
        #page = self.getpage()
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page.decode('utf-8'))
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
        #获取页数
        #page = self.getpage()
        pattern = re.compile('<span class="red">(.*?)</span>', re.S)
        result = re.search(pattern, page.decode('utf-8'))
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPersonName(self,page):

        pattern = re.compile('<a data-field.*?>(.*?)</a>', re.S)
        items  = re.findall(pattern, page.decode('utf-8'))
        persons = []
        p = Tool()
        for item in items:
            person=  p.replace(item)
            persons.append(person)
        return persons
    def getContent(self, page):
        #获取内容
        #page = self.getpage()
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page.decode('utf-8'))
        contents = []
        p = Tool()
        for item in items:
            content = p.replace(item)
            contents.append(content)



        return contents
    def getContentTime(self, page):
        #获取内容
        #page = self.getpage()
        pattern = re.compile('<span class="tail-info">\d{4}-\d{2}-\d{2} \d{2}:\d{2}</span>', re.S)
        items = re.findall(pattern, page.decode('utf-8'))
        contents = []
        p = Tool()
        for item in items:
            content =  p.replace(item)
            contents.append(content)
        return contents

    def getIndexPage(page):
        # 获取内容
        # page = self.getpage()
        pattern = re.compile('<a data-tid.*?href="([^"]*)"', re.S)
        items = re.findall(pattern, page.decode('utf-8'))
        contents = []
        p = Tool()
        for item in items:
            content = p.replace(item)
            contents.append(content)
        return contents
    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + ".txt" ,"wb")
        else:
            self.file = open(self.defaultTitle + ".txt", "wb")

    def writeData2CSV(self,tiebaName,title ,PersonName,contents,contentTime):
        # 数据按列存储为list
        tiebaNames = [tiebaName for i in range(len(PersonName)) ]
        titles = [title for i in range(len(PersonName)) ]
        rawData = [tiebaNames,titles,PersonName,contents,contentTime]
        wData = list(zip(*rawData))
        encodeData = []
        data = [['贴吧名', '帖子标题', 'ID','内容', '发布时间']]
        for i in wData:
            data.append(i)
        for i in data:
            tmp = []
            for j in i :
                tmp.append(emojiswitch.demojize(j,delimiters=("_","_"),lang="zh"))
            encodeData.append(tmp)
        # create and open CSV file
        with open('../src/SinglePost/'+ tiebaName+ '_'+title+'.csv', 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)

            # write data
            writer.writerows(encodeData)

        with open('../src/TotalPost/data.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)

            # write data
            writer.writerows(encodeData)
    def start(self):
        indexPage = self.getpage(1)
        pageNum = self.getPageNum(indexPage)
        tiebaName = self.getFname(indexPage)

        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print ("URL无效，请重试")
            return
        try:
            print (u"该帖子共有" + str(pageNum) + u"页")
            for i in range(1, int(pageNum)+1):
                print ("正在写入第" + str(i) + "页数据")
                page = self.getpage(i)
                PersonName = self.getPersonName(page)
                contentTime = self.getContentTime(page)
                contents = self.getContent(page)
                self.writeData2CSV(tiebaName ,title,PersonName,contents,contentTime)
        except IOError as  e:
            print ("写入异常，原因"+ e.message)
        finally:
            print ("写入任务完成")

    def initilize(self,url):
        AllPage = self.getpage(1)