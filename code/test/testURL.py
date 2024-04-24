# -*- coding:utf-8 -*-
import urllib
import urllib.request
import re
import csv
import emojiswitch
from ToolFunction import BDTB
from ToolFunction import load_list_from_txt
from ToolFunction import save_config,read_config

# PostURLListPath = "../src/PostURLList/list_data.txt"
# PostURLList = load_list_from_txt(PostURLListPath )


# baseURL = 'http://tieba.baidu.com/p/8964732662?pid=150049805947&cid=0#150049805947'
# seeLZ = 0  #input("是否只看楼主，是请输入1\n")
# floorTag = 1  #input("是否写入楼层信息，是输入1\n")
# bdtb = BDTB(baseURL,seeLZ,floorTag)
# bdtb.start()

config ={"startnum": 1 , "totalnum":70,"keyword":"离婚冷静期"}
save_config(config)














