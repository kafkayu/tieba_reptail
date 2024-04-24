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

# Acknoledgement

部分代码来自于[linyha](https://github.com/linyha/tieba) , 构建IP池部分来自[博客](https://www.cnblogs.com/TurboWay/p/8172246.html),感谢新传学院相关学长和老师需求建议

