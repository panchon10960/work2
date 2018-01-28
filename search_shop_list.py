
# SHOP_NAME = 'clothes2017'
# SHOP_NAME = 'minervasea'
import urllib.request, urllib.parse
from urllib.request import urlopen
import json
import pymysql
import sys
import os
from os.path import abspath, dirname, join
import pprint
import time

pymysql.install_as_MySQLdb()

NETSHOP_PROJECT_PATH = join(dirname(dirname(abspath(__file__))), 'netshop')
sys.path.append(NETSHOP_PROJECT_PATH)
os.environ["DJANGO_SETTINGS_MODULE"] = "netshop.settings"

import django
django.setup()
from django.forms import model_to_dict
from django.db import transaction
from polls.models import BaseFromAPI
from django.db import transaction

def download(url, path):
    os.chdir(path)
    if urlopen(url):
        img = urlopen(url)
        localfile = open(os.path.basename(url), 'wb')
        localfile.write(img.read())
        img.close()
        localfile.close()

def saveBySize(item, size):
    data = {}
    if item['item_id'] is not None:
        data['item_id'] = str(item['item_id'])
    if item['img1_origin'] is not None:
        data['image1'] = item['img1_origin']
    if item['img2_origin'] is not None:
        data['image2'] = item['img2_origin']
    if item['img3_origin'] is not None:
        data['image3'] = item['img3_origin']
    if item['img4_origin'] is not None:
        data['image4'] = item['img4_origin']
    if item['img5_origin'] is not None:
        data['image5'] = item['img5_origin']
    if size is not None:
        data['size'] = size
    if item['title'] is not None:
        data['title'] = item['title'].replace('即納', '').replace('送料無料', '')
    if item['detail'] is not None:
        data['discription2'] = item['detail']
    if item['price'] is not None:
        data['price'] = item['price']
    if item['shop_id'] is not None:
        data['shop_name'] = item['shop_id']
    if item['categories'][0] is not None:
        data['category_1'] = item['categories'][0]
    data['is_csv'] = 0

    with transaction.atomic():
        base_from_api = BaseFromAPI(**data)
        base_from_api.save()

if __name__ == "__main__":
    params_items = {'start' : 0, 'size' : 50}
    API_HOST = 'https://api.thebase.in'
    API_VERSION = 1
    REDIRECT_URI = 'http://tenshoku.top/callback'
    URL = 'https://api.thebase.in/1/search'
    SHOP_NAME = 'lieblingshop'

    save_base_data_path = '/Volumes/remote_disk/base_api/'
    os.chdir(save_base_data_path)

    shop_path = '/Volumes/remote_disk/base_api/' + SHOP_NAME + '/'

    if os.path.exists(shop_path):
        pass
    else:
        os.mkdir(SHOP_NAME)

    start = 0
    size = 50
    html = ''
    while(html is not None):
        time.sleep(1)
        pprint.pprint(start)
        pprint.pprint(size)

        params = {
          'client_id' : 'b63030e019980dcfc087867558fe3dbb',
          'client_secret' : '90354a8ec56815d15f9975ce4f4da658',
          'q' : '*',
          'shop_id' : SHOP_NAME,
          'start' : start,
          'size' : size,
        }
        parameters = urllib.parse.urlencode(params)
        url = URL + '?' + parameters

        with urllib.request.urlopen(url) as res:
           html = res.read().decode("utf-8")
           json_dict = json.loads(html)
           for item in json_dict['items']:
               if item['categories'][0]:
                   shop_category_path = shop_path + item['categories'][0] + '/'
                   if os.path.exists(shop_category_path):
                       pass
                   else:
                       os.mkdir(shop_category_path)
               if item['detail']:
                   if item['detail'].find('XS') > -1:
                       saveBySize(item, 'XS')
                   if item['detail'].find('S') > -1:
                       saveBySize(item, 'S')
                   if item['detail'].find('M') > -1:
                       saveBySize(item, 'M')
                   if item['detail'].find('L') > -1:
                       saveBySize(item, 'L')
                   if item['detail'].find('XL') > -1:
                       saveBySize(item, 'XL')

               images = []
               if item['img1_origin']:
                   images.append(item['img1_origin'].split('/')[-1])
               if item['img2_origin']:
                   images.append(item['img2_origin'].split('/')[-1])
               if item['img3_origin']:
                   images.append(item['img3_origin'].split('/')[-1])
               if item['img4_origin']:
                   images.append(item['img4_origin'].split('/')[-1])
               if item['img5_origin']:
                   images.append(item['img5_origin'].split('/')[-1])
               for image in images:
                   time.sleep(1)
                   download(image, shop_category_path)

        start += 50
        size += 50
