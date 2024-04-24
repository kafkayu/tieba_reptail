# -*- coding:utf-8 -*-
import urllib
import urllib.request
import re
import csv
import emojiswitch
from ToolFunction import BDTB
from ToolFunction import load_list_from_txt


PostURLListPath = "../src/PostURLList/list_data.txt"
PostURLList = load_list_from_txt(PostURLListPath )
needTitle = 1
for PostURL in PostURLList:

        baseURL = 'http://tieba.baidu.com' + PostURL
        seeLZ = 0  #input("是否只看楼主，是请输入1\n")
        floorTag = 1  #input("是否写入楼层信息，是输入1\n")

        bdtb = BDTB(baseURL,seeLZ,floorTag,needTitle)
        needTitle = 0
        bdtb.start()

















