# -*- coding: utf-8 -*-
# -*- coding: latin-1 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from products.models import Product

import json
from ast import literal_eval
class MyteckScrapingPipeline(object):
    def process_item(self, item, spider):
    	# obj = Product.objects.get_or_create(name=item['name'],price=item['price'])
    	pr = Product()
    	n = item['name']
    	p = item['price']
    	img = item["image_url"]
    	c = item['category']
    	sc = item['sub_category']
    	addr = item['addr_pr']
    	st = item["store"]
    	# # i = 2
    	# # while i<len(i)-1:
    	# # 	pr.name = n[i]
    	# # 	i+=1
    	pr.name = (literal_eval(json.dumps(n[0]))).decode('unicode-escape')
    	pr.price = literal_eval(json.dumps(p[0]))
    	pr.image_url = (literal_eval(json.dumps(img[0]))).decode('unicode-escape')
    	pr.category = (literal_eval(json.dumps(c))).decode('unicode-escape')
    	pr.sub_category = sc
    	pr.store = st
    	pr.addr_pr = (literal_eval(json.dumps(addr[0]))).decode('unicode-escape')
    	# pre = dict(pr)
    	# pre.save()
    	pr.save()
     #    # l = json.dumps(dict(item))
        # item.save()
        return item


	# def cleanup_data(self, data):
 #   		return data[0:m.end(1)]