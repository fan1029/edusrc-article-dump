# edusrc-article-dump
用来导出edusrc的文章
目前快完成了 基本功能有了 不过有小概率导出会失败 过几天修了 
-------------------------------------------------------------
使用前请需要把自己账号的COOKIE放到里面
初始化一个新对象
user=User("csrftoken","sessionid")
使用
user.dump_articles()
会导出文章到当前目录 名称为漏洞ID
---------------------
需要安装的库
requests   lxml
