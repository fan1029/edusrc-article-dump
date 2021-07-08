import requests
from lxml import etree
import re

class User:
    def __init__(self,csrftoken,sessionid):
        self.csrftoken=csrftoken
        self.sessionid=sessionid

    def get_article_html(self,id):
        pt1 = '<header class="am-topbar am-g am-g-collapse">.*</header>'
        pt2 = '<div class="main-footer">.*?</div>'
        burp0_url = "https://src.sjtu.edu.cn:443/post/"+id+"/"
        burp0_cookies = {"csrftoken": self.csrftoken,
                         "sessionid": self.sessionid}
        burp0_headers = {"Cache-Control": "max-age=0",
                         "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
                         "Sec-Ch-Ua-Mobile": "?0", "Upgrade-Insecure-Requests": "1",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                         "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                         "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                         "Accept-Language": "zh-CN,zh;q=0.9",
                         "Connection": "close"}
        text = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies).text
        text = re.sub(pt1, "", text, flags=re.DOTALL)
        text = re.sub(pt2, "", text, flags=re.DOTALL)
        return text


    def send(self,page=1):
        burp0_url = "https://src.sjtu.edu.cn:443/profile/?page="+str(page)
        burp0_cookies = {"csrftoken": self.csrftoken,
                         "sessionid": self.sessionid}
        burp0_headers = {"Cache-Control": "max-age=0",
                         "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
                         "Sec-Ch-Ua-Mobile": "?0", "Upgrade-Insecure-Requests": "1",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                         "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                         "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                         "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
        text = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies).text
        return text
    def get_page(self):
        text = self.send()
        html = etree.HTML(text)
        a2 = html.xpath('/html/body/div/div/div[1]/div/div/div/div[3]/ul/li')
        page_ele=a2[-2]
        e=page_ele.xpath('./a/@href')
        pt1='\?page=(.*)'
        page=re.search(pt1,e[0]).group(1)
        return page

    def get_article_id(self):
        urls=[]
        ids=[]
        max_page=self.get_page()
        for i in range(1,int(max_page)+1):
            text=self.send(page=i)
            html=etree.HTML(text)
            a1=html.xpath('/html/body/div/div/div[1]/div/div/div/table/tr')
            for i in a1[1:]:
                url=i.xpath('./td[2]/a/@href')[0]
                urls.append(url)
        for url in urls:
            pt="\d+"
            aa=re.search(pt,url).group(0)
            ids.append(aa)
        print("文章ID获取完成")
        return ids


    def dump_articles(self):
        ids=self.get_article_id()
        for id in ids:
            print("当前"+id)
            text=self.get_article_html(id)
            article_html = etree.HTML(text)
            c = article_html.xpath('/html/body/div/div/div[1]/div/div/article')
            try:
                imgs = c[0].xpath('.//@src')
                for i in imgs:
                    new = "https://src.sjtu.edu.cn/" + i
                    if i in text:
                        text = text.replace(i, new)
                name=1
                with open(id+".html", "a+", encoding="utf-8") as f:
                    for i in text:
                        f.write(i)
            except:
                print(id+"错误")





user=User("csrftoken","sessionid")
user.dump_articles()