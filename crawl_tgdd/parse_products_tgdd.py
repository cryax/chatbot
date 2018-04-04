from BeautifulSoup import BeautifulSoup
import requests


def parse_href(raw_text):
    count = 0
    lists = []
    
    soup = BeautifulSoup(raw_text)
    
    for a in soup.findAll('a', href=True):
        count += 1
        lists.append(a['href'])
    return lists

def get_from_post(list_link):
    for i in range(6):
        r = requests.post("https://www.thegioididong.com/aj/CategoryV5/Product", 
                      data={'Category': 42, 
                            'PageSize': 30,
                            'PageIndex': i+1, 
                            'ClearCache': 0})
        list_link.append(parse_href(r.text))
    return list_link

list_link = []
list_link = get_from_post(list_link)
flat_list = [item for sublist in list_link for item in sublist]
flat_list = filter(lambda x: 'dtdd' in x, flat_list)
f = open('links.txt', 'w')
flat_list = map(lambda x: x + '\n', flat_list)
f.writelines(list(set(flat_list)))
f.close()