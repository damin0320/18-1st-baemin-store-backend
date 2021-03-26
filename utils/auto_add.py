import requests
import csv
import json
import random
import time

from my_settings import DOMAIN_URL


f = open('baemin_data.csv', 'r')
rdr = csv.reader(f)


for i, col in enumerate(rdr):
    if i == 0 or i == 1:
        continue
    
    data_ = {
             'category_name': col[0],
             'sub_category_name': col[1],
             'product_name': col[2],
             'price': col[3],
             'thumbnail': col[4],
             'images': [col[5]],
             'stock': col[6],
             'discount_rate': col[7],
             'option_classification': col[8],
             'material': col[9],
             'size_cm': col[10],
             'manufacture_country': col[11],
             'caution': col[12],
             'options': json.loads(col[13]) if col[13] else [],
             'publisher': random.choice(['김택향', '김미현', '안다민', '최송희', '홍래영']),
             'total_page': random.choice([300, 400, 500, 122, 133, 144, 250, 320]),
             'size_mm': random.choice(['222mm X 333mm', '250mm X 350mm', '230mm x 250mm'])
            }
    
    data = json.dumps(data_)

    s = requests.session()
    res = s.post(DOMAIN_URL + '/product', data=data)
    time.sleep(0.1)
