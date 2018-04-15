# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
from time import time
import random
from functools import wraps
import datetime
import os
import bs4

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print ('func:%r args:{%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap

def read_files():
    path = './html-pages/'
    
    data_list = []
    def read_data(file_path):
        text_file = open(file_path, "r")
        lines = text_file.readlines()
        return lines
    for filename in os.listdir(path):
        
        data = read_data(path+filename)
        data = ' '.join(e for e in data)
        product_name = filename.split('.html')[0][13:]
        soup = bs4.BeautifulSoup(data, "lxml")
        for ultag in soup.findAll('q'):
            content = ultag.text
            content = content.replace(',','--COMMA--')
            content = content.replace('"','')
            content = content.replace("'",'')
            data_list.append([product_name, content])
    print('done reading')
    return data_list
        
def write_data(datas):
    csv = open("data.csv", "w") 

    columnTitleRow = "product, content\n"
    csv.write(columnTitleRow)

    for data in datas:
        data_mention = data[1]
        # data[1] = data[1].replace(",", "--COMMA--")
        row = data[0] + "," + data[1] + "\n"
        csv.write(row)

@timing
def doshit():
    client = MongoClient('mongodb://158.69.249.39:27018')
    db = client.rnd
    collection = db.questions_tgdd
    datas = []
    data_2_insert = [{"a":22}]
    print("start to read data from files")
    datas = read_files()
    print("Done read data from files")
    for data in datas:
        data_2_insert.append({
            "product": data[0],
            "content": data[1]
        })
    print(len(data_2_insert))
    # collection.insert(data_2_insert)
    
datas = read_files()
write_data(datas)