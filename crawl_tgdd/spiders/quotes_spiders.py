import scrapy
import bs4
import re
import requests

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
        
        urls = ['https://www.thegioididong.com/dtdd/oppo-f5-6gb']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        count = 0
        path = '/home/dangpham/Dann/source_code/scrapy/crawl_tgdd/html-pages/'
        page = response.url.split("/")[-2]
        filename = 'test_content-%s.html' % page
        content = []
        max_page, product_id = find_maxpage_productid(response.body)
        max_page = 10
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
            content += r.text + '\nNEXT PAGE \n'
        with open(path+filename, 'w') as f:
            f.write(content)
        self.log('Saved file %s' % filename)
