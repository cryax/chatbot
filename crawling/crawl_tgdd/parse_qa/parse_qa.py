# -*- coding: utf-8 -*-
import bs4

def parser_qafc(file_name, content):
    soup = bs4.BeautifulSoup(content.decode('utf-8'), "lxml")
    count = 0
    parsed_qa = []
    
    for ultag in soup.findAll('li', {'class': 'comment_ask'}):

        for litag in ultag.find_all('div', {'class': 'question'}):
            parsed_qa.append('<q>')
            parsed_qa.append(litag.text)
            parsed_qa.append('<q>')
            parsed_qa.append('\n')
        for lirep in ultag.find_all('div', {'class': 'cont'}):
            parsed_qa.append('<a>')
            parsed_qa.append(lirep.text)
            parsed_qa.append('<a>')
            parsed_qa.append('\n')
    with open(filename, 'w+') as f:
            f.write(parsed_qa)
    f.close()


file_html = open('/media/younet/DATA/dang/source_code/chatbot/crawling/crawl_tgdd/crawl_tgdd/parse_qa/html.txt', 'r')
html = file_html.read()
soup = bs4.BeautifulSoup(html.decode('utf-8'), "lxml")
count = 0
for ultag in soup.findAll('li', {'class': 'comment_ask'}):
    # count+=1
    # print(ultag)
    for litag in ultag.find_all('div', {'class': 'question'}):
        print('<q>')
        print(litag.text)
        print('<q>')
        print('\n')
    for lirep in ultag.find_all('div', {'class': 'cont'}):
        print('<a>')
        print(lirep.text)
        print('<a>')
        print('\n')
print(count)