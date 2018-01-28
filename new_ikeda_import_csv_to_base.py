import pymysql
import sys
import os
import pprint
import random
pymysql.install_as_MySQLdb()

from os.path import abspath, dirname, join

NETSHOP_PROJECT_PATH = join(dirname(dirname(abspath(__file__))), 'netshop')
sys.path.append(NETSHOP_PROJECT_PATH)
os.environ["DJANGO_SETTINGS_MODULE"] = "netshop.settings"

import django
django.setup()
from django.forms import model_to_dict
from django.db import transaction
from polls.models import Buyma
import pandas as pd
from pprint import pprint

title = ""

discription2 = """

※お客様ご使用のPC環境により商品画像のカラーが多少異なる場合があります。
予めご了承ください。

""".encode('CP932', 'ignore').decode('CP932')

category_name = "ワンピース・オールインワン"
shop_name = 2089482
# buyma_list = Buyma.objects.filter(is_csv=0).filter(shop_name=shop_name, category_name=category_name).order_by('title').order_by('image1')[:2000].values()
buyma_list = Buyma.objects.filter(is_csv=0).filter(shop_name=shop_name, category_name=category_name).order_by('title').order_by('image1').values()
csv_list = []
previous_title = ""

with transaction.atomic():
    for buyma in buyma_list:
        # update_buyma = Buyma.objects.filter(id=buyma['id']).first()
        # update_buyma.is_csv = 1
        # update_buyma.save()
        total_discription = ""
        if buyma['discription2'] is not None:
            total_discription += str(buyma['discription2']) + '\n'
        if buyma['discription1'] is not None:
            if buyma['discription2'].find('バスト') == -1:
                if buyma['discription2'].find('胸囲') == -1:
                    total_discription += str(buyma['discription1'].replace('【サイズ】', ''))

        total_discription += discription2

        if buyma['title'].find('Chicwish') > -1 or buyma['title'].find('Little Mistress') > -1 or buyma['title'].find('Chi Chi London') > -1 or buyma['title'].find('Lipsy') > -1 or buyma['title'].find('メゾン・マルタン・マルジェラ') > -1 or buyma['title'].find('Dsquared2') > -1 or buyma['title'].find('Marc Jacobs') > -1 or buyma['title'].find('Just Cavalli') > -1 or buyma['title'].find('VIKTOR & ROLF') > -1 or buyma['title'].find('TED BAKER') > -1 or buyma['title'].find('Free People') > -1 or buyma['title'].find('Reclaimed Vintage') > -1 or buyma['title'].find('ASOS') > -1:
            pass
        else:
            csv_list.append(
                [title + buyma['title'].encode('CP932', 'ignore').decode('CP932'),
                total_discription,
                str(int(buyma['price'])),
                "10",
                "1",
                "",
                buyma['size'],
                random.randint(5,10),
                buyma['image1'],
                buyma['image2'],
                buyma['image3'],
                buyma['image4'],
                buyma['image5']])

            df = pd.DataFrame(
                csv_list,
                columns=[
                    '商品名',
                    '説明',
                    '価格',
                    '在庫数',
                    '公開状態',
                    '表示順',
                    '種類名',
                    '種類在庫数',
                    '画像1',
                    '画像2',
                    '画像3',
                    '画像4',
                    '画像5'
                ])

            df.to_csv("onepiece.csv", encoding="cp932", index=False)
