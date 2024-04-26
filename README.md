# Introdution
这是根据某个搜索词，爬取百度贴吧所有相关帖子及用户的评论详情的demo

# Envrionment
python == 3.8  
urllib  
re  
csv  
emojiswitch  
json

# Function
1. 实现对于搜索界面所有帖子链接爬取
2. 实现对于所有帖子链接爬取具体相关内容，包括贴吧名字，帖子标题，用户名字，用户发帖内容，用户发帖时间
3. 对于用户评论表情包进行翻译，翻译为中文

# File structure
> code 文件包含所有实现代码

>> test 文件夹包含测试代码，可能有路径上错误，使用时请自行修改

>> getURL.py 实现对于搜索关键字获取所有相关帖子链接

>> tieba.py 实现对于已知URL下获得帖子内容

>> ToolFunction.py 实现

> src 文件夹包含资源文件

>> config 配置参数

>> HtmlList 爬取所有网页

>> PostURLList 所有帖子URL链接

>> SinglePost 单个帖子信息

>> TotalPost 所有帖子信息

# Tutor
```
python getURL.py #####运行获得所有相关帖子URL并保存再PostURLList，保存爬取网页在HtmlList

python tieba.py ####获得所有帖子内容
```

# Debug
## 运行tieba.py时 URL错误，返回数据为None等问题
解决方法：原因是百度贴吧对于经常访问的异常IP进行了一些过滤和验证，解决方法是更换网络，比如使用不同VPN作为代理，或者使用流量访问等。经实测，使用数据访问最为稳定，但是要考虑流量费用，使用WIFI有一定效果，但是没有流量稳定，使用VPN访问有一定效果，但是容易被当成异常IP被封。总体来说，推荐网络：数据>WIFI>VPN



# Future work
正在尝试构建IP POOL尝试绕过一些反扒机制，目前参考的github有[IP POOL](https://github.com/xiaosimao/IP_POOL)

# Acknoledgement

部分代码来自于[linyha](https://github.com/linyha/tieba) , 构建IP池部分来自[博客](https://www.cnblogs.com/TurboWay/p/8172246.html),感谢新传学院相关学长和老师需求建议

