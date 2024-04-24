######################################
# File: tieba.py
# Author: Jiahong Yu
# Created: 2024-04-24
# Last Modified: 2024-04-24
# Description: This is an main file which search and get post content
######################################
# -*- coding:utf-8 -*-
import urllib
import urllib.request
import re
import csv
import emojiswitch
from ToolFunction import BDTB
from ToolFunction import load_list_from_txt
from ToolFunction import save_config,read_config,save_list_to_txt

PostURLListPath = "../src/PostURLList/list_data.txt"
PostURLList = load_list_from_txt(PostURLListPath )
needTitle = 1
config = read_config()
startURL = config["startURL"]
print("The total num of URL is: ",len(PostURLList))

for index,PostURL in enumerate(PostURLList):
        if index >0 : needTitle=0
        if index>startURL:
                baseURL = 'http://tieba.baidu.com' + PostURL
                seeLZ = 0  #input("是否只看楼主，是请输入1\n")
                floorTag = 1  #input("是否写入楼层信息，是输入1\n")
                bdtb = BDTB(baseURL,seeLZ,floorTag,needTitle)
                res = bdtb.start()
                #######renew the config
                config["startURL"] = index
                save_config(config)
                if res ==False:
                        data = [PostURL]
                        save_list_to_txt(data , "../src/PostURLList/wrongURL.txt")

















