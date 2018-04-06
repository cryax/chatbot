import scrapy
import bs4
import re
import requests

def parser_qafc(file_name, content):
    soup = bs4.BeautifulSoup(content, "lxml")
    count = 0
    parsed_qa = ""
    
    for ultag in soup.findAll('li', {'class': 'comment_ask'}):

        for litag in ultag.find_all('div', {'class': 'question'}):
            parsed_qa+='<q>'
            parsed_qa+=litag.text
            parsed_qa+='</q>'
            parsed_qa+='\n'
        for lirep in ultag.find_all('div', {'class': 'cont'}):
            parsed_qa+='<a>'
            parsed_qa+=lirep.text
            parsed_qa+='<a>'
            parsed_qa+='\n'
    with open(file_name, 'w+') as f:
            f.write(parsed_qa)
    f.close()

def find_maxpage_productid(html):
    soup = bs4.BeautifulSoup(html)

    product_id = soup.find(id='ProductId').get("value")
    a_tags = soup.find_all("a")
    list_pages_num = []
    for tag in a_tags:
        # cc = tag.find(text=re.compile('\d+'))
        cc = tag.get('title')
        if(cc):
            if ('trang' in cc) and (cc.count(" ")==1):
                _, page_num = cc.split()
                list_pages_num.append(int(page_num))
    max_page = max(list_pages_num)
    return max_page, product_id

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        f = open('/home/dangpham/Dann/source_code/scrapy/crawl_tgdd/crawl_tgdd/spiders/list_product', 'r')
        pages = f.readlines()
        pages = map(lambda x: 'https://www.thegioididong.com'+x.replace('\n',''), pages)
        for url in pages:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        count = 0
        path = '/home/dangpham/Dann/source_code/scrapy/crawl_tgdd/html-pages/'
        page = response.url.split("/")[-1]
        filename = 'test_content-%s.html' % page
        content = []
        max_page, product_id = find_maxpage_productid(response.body)
        content = ""
        for i in range(max_page+1):
            r = requests.post("https://www.thegioididong.com/commentnew/cmt/index?callback=jQuery18301935113702865583_1521652490455", 
                    data={'core[ajax]': True, 
                        'core[call]': 'cmt.listpaging',
                        'pageSize': 5, 
                        'objectid': 114111,
                        'objecttype': 2,
                        'siteID': i+1,
                        'pageindex': 1,
                        'Type': 2,
                        'order': 1,
                        'core[security_token]': 'wPj1I'})
            print(type(r.text))
            content += r.text
        parser_qafc(path+filename, content) 
        # with open(path+filename, 'w+') as f:
        #     f.write(content)
        self.log('Saved file %s' % filename)
