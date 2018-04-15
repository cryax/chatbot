from flask import Flask, request
import os
import json
import ast
import random
import urllib 
from sshtunnel import SSHTunnelForwarder
import pymongo

questions_collection = 'questions_tgdd'
labeld_collection = 'labeled_questions_tgdd'
MONGO_HOST = "158.69.249.39"
MONGO_DB = "rnd"
MONGO_USER = "cicd"
MONGO_PASS = "uNVm@N&{7t-}*ZmB"
list_product = ["samsung-e1200", "sony-xperia-xzs", "oppo-f5-youth", "htc-one-a9s", "htc-10-evo", "itel-it5020", "sony-xa1-ultra", "motorola-moto-e4-plus", "xiaomi-mi-a1", "asus-zenfone-4-max-pro-zc554kl", "xiaomi-mi-a1-32gb", "xiaomi-redmi-5-plus", "mobiistar-b821-trang", "mobiistar-b310", "mobiistar-b821", "huawei-y7-pro-2018", "mobiistar-prime-x-max-2018", "asus-zenfone-live-zb501kl", "vivo-1606-y53", "mobiistar-lai-z1", "htc-u-ultra", "huawei-y5-2017", "sony-xperia-xz-premium-pink-gold", "philips-e168", "asus-zenfone-max-plus-m1-zb570tl", "nokia-150-khong-the-nho", "philips-e181", "mobell-m339", "vivo-1713-v5s", "motorola-moto-c-plus", "mobell-s40", "htc-u-play", "motorola-moto-g5s-plus", "philips-s327", "philips-s329", "sony-xperia-l1", "huawei-nova-3e", "nokia-230-khong-the", "xiaomi-redmi-4x", "nokia-6", "sony-xperia-x", "mobell-rock-3", "motorola-moto-c-4g", "mobell-nova-i6", "iphone-8-plus", "samsung-galaxy-c9-pro", "vivo-v7-plus", "vivo-v9", "philips-e570", "mobiistar-lai-yuna-1", "huawei-nova-2i", "itel-it2123", "iphone-6s-32gb", "samsung-galaxy-a8-2018", "sony-xepria-xa1-plus", "nokia-8", "mobell-m889", "nokia-105-single-sim-2017", "philips-e316", "mobiistar-zumbo-s-lite-2017", "iphone-x-64gb", "philips-e105", "itel-it5630", "iphone-7-plus", "mobell-m389", "xiaomi-redmi-note-5a", "samsung-galaxy-j7-pro", "nokia-5", "sony-xperia-xa1-plus-vang", "sony-xperia-xz1", "mobiistar-zumbo-s2-dual", "mobiistar-lai-zoro-lte", "iphone-7", "nokia-130-2017", "itel-it1516-plus", "vivo-y69", "itel-it1508-plus", "sony-xperia-l2", "sony-xperia-xa-ultra", "samsung-galaxy-note8", "samsung-galaxy-a8-plus-2018", "itel-p51", "samsung-galaxy-j3-pro-2017", "itel-it2180", "motorola-moto-x4", "mobell-nova-p3", "mobiistar-zumbo-s-2017", "iphone-8-64gb", "oppo-f3-plus", "sony-xperia-xz-premium", "iphone-x-256gb", "samsung-galaxy-s8-plus", "mobiistar-b221-2017", "sony-xperia-xz", "iphone-6-32gb-gold", "samsung-galaxy-s9-plus-128gb", "mobell-s50", "philips-e331", "oppo-f5-6gb", "samsung-galaxy-s9", "oppo-a37-a37fw", "nokia-105-2017", "oppo-f5", "mobell-nova-f7-pro", "iphone-8-plus-256gb", "nokia-216-khong-the", "mobiistar-zumbo-j2", "mobell-m228", "sony-xperia-xa1", "samsung-galaxy-a7-2017", "itel-a13", "huawei-y3-2017", "xiaomi-redmi-note-4", "oppo-a71-2018", "mobell-nova-i4", "iphone-7-plus-128gb", "mobiistar-lai-zumbo-s2", "nokia-3", "mobell-m529", "mobiistar-zumbo-power", "sony-xperia-l1-trang", "oppo-a83", "samsung-galaxy-j2-prime", "samsung-galaxy-j3-lte", "samsung-galaxy-j2-pro-2018", "samsung-galaxy-j7-plus", "nokia-3310-2017", "bkav-bphone-2", "xiaomi-redmi-note-5a-prime", "mobell-s30", "mobiistar-b248i", "mobell-m789", "mobiistar-b242i", "huawei-y7-prime", "oppo-a57", "itel-it7100", "asus-zenfone-4-max-zc520kl", "samsung-galaxy-j7-prime", "motorola-moto-z2-play", "itel-s31", "samsung-galaxy-s8", "asus-zenfone-2-go-zb500kg", "itel-s11-plus", "itel-it5070", "nokia-2", "philips-e103", "samsung-galaxy-s9-plus", "mobiistar-lai-z2", "iphone-8-256gb", "philips-e170", "itel-it5232", "vivo-v7", "philips-e106", "sony-xperia-xa1-ultra-pink", "itel-it5602", "vivo-1610-y55s"]
server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 27018)
)
server.start()
# client = pymongo.MongoClient('127.0.0.1', 27017)
client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
cl = client['rnd'][questions_collection]

app = Flask(__name__)
@app.route('/api/get_questions', methods=['GET'])
def get_topics_collection():
    random_product = random.choice(list_product)
    pipeline = [
        {"$match": {"product": random_product}},
        {"$sample": {"size": 1}}
    ]
    result = (list(cl.aggregate(pipeline)))
    
    result = result[0]['content']
    data = {'content': result, 'product': random_product}
    return json.dumps(data)

@app.route('/api/save_labeled_questions', methods=['POST'])
def save_labeled_question():
   
    data = request.json
    if("content" not in data) or ("product" not in data):
        return "Error"
    cl_save_labeled = client['rnd'][labeld_collection]
    cl_save_labeled.insert(data)
    return "OK"


app.run(host='0.0.0.0', port=8010)
