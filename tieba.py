# -*- coding:utf-8 -*-
import urllib
import urllib.request
import re
import csv
import emojiswitch

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

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + ".txt" ,"wb")
        else:
            self.file = open(self.defaultTitle + ".txt", "wb")

    def writeData(self, tiebaName ,PersonName,contents,contentTime):

        self.file.write(tiebaName.encode("utf-8"))
        for item in PersonName:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + "------------------------------------------------ \n"
                self.file.write(floorLine.encode("utf-8"))
            self.file.write(item.encode("utf-8"))
            self.floor += 1

        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + "------------------------------------------------ \n"
                self.file.write(floorLine.encode("utf-8"))
            self.file.write(item.encode("utf-8"))
            self.floor += 1

        for item in contentTime:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + "------------------------------------------------ \n"
                self.file.write(floorLine.encode("utf-8"))
            self.file.write(item.encode("utf-8"))
            self.floor += 1
    def writeData2CSV(self,tiebaName,title ,PersonName,contents,contentTime):
        # 数据按列存储为list
        tiebaName = [tiebaName for i in range(len(PersonName)) ]
        title = [title for i in range(len(PersonName)) ]
        rawData = [tiebaName,title,PersonName,contents,contentTime]
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
        # 创建并打开CSV文件
        with open('data.csv', 'w', newline='',encoding='utf-8-sig') as file:
            writer = csv.writer(file)

            # 写入数据行
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


print ("请输入帖子代号")
baseURL = 'http://tieba.baidu.com/p/' + '8964732662?pid=150049805947&cid=0#150049805947'
          #str(input(u'http://tieba.baidu.com/p/'))
seeLZ = 0#input("是否只看楼主，是请输入1\n")
floorTag = 1#input("是否写入楼层信息，是输入1\n")
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()

















