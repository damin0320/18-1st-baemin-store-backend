import requests
import csv
import json
import random
import time


f = open('baemin_data_last.csv', 'r')
rdr = csv.reader(f)


for i, col in enumerate(rdr):
    if i == 0 or i == 1:
        continue

    if not col[3]:
        continue
    
    options_raw = json.loads(col[13]) if col[13] else []
    options = []
    if options_raw:
        for option in options_raw:
            option_stock = int(option['option_stock'])
            additional_price = float(option['additional_price'])
            option_name = option['option_name']

            options.append({'option_name': option_name, 'option_stock': option_stock, 'additional_price':additional_price})

    data_ = {
             'category_name': col[0],
             'sub_category_name': col[1],
             'product_name': col[2],
             'price': float(col[3]),
             'thumbnail': col[4],
             'images': [col[5]],
             'stock': col[6],
             'discount_rate': col[7],
             'option_classification': col[8],
             'material': col[9],
             'size_cm': col[10],
             'manufacture_country': col[11],
             'caution': col[12],
             'options': options,
             'publisher': random.choice(['김택향', '김미현', '안다민', '최송희', '홍래영']),
             'total_page': random.choice([300, 400, 500, 122, 133, 144, 250, 320]),
             'size_mm': random.choice(['222mm X 333mm', '250mm X 350mm', '230mm x 250mm'])
            }
    
    data = json.dumps(data_)

    s = requests.session()
    res = s.post('http://localhost:8000/product', data=data)
    time.sleep(0.05)
