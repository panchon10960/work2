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
from polls.models import BaseFromAPI
import pandas as pd
from pprint import pprint

title = ""

discription2 = """

※お客様ご使用のPC環境により商品画像のカラーが多少異なる場合があります。
予めご了承ください。

""".encode('CP932', 'ignore').decode('CP932')

category_1 = "トップス"
shop_name = 'Lieblingshop'
# base_list = BaseFromApi.objects.filter(is_csv=0).filter(shop_name=shop_name, category_1=category_name).order_by('title').order_by('image1')[:2000].values()
base_list = BaseFromAPI.objects.filter(is_csv=0).filter(shop_name=shop_name, category_1=category_1).order_by('title').order_by('image1').values()
csv_list = []
previous_title = ""

with transaction.atomic():
    for base in base_list:
        # update_buyma = Buyma.objects.filter(id=base['id']).first()
        # update_buyma.is_csv = 1
        # update_buyma.save()
        total_discription = ""
        if base['discription2'] is not None:
            total_discription += str(base['discription2']) + '\n'
        if base['discription1'] is not None:
            if base['discription2'].find('バスト') == -1:
                if base['discription2'].find('胸囲') == -1:
                    total_discription += str(base['discription1'].replace('【サイズ】', ''))

        total_discription += discription2

        if base['title'].find('Chicwish') > -1 or base['title'].find('Little Mistress') > -1 or base['title'].find('Chi Chi London') > -1 or base['title'].find('Lipsy') > -1 or base['title'].find('メゾン・マルタン・マルジェラ') > -1 or base['title'].find('Dsquared2') > -1 or base['title'].find('Marc Jacobs') > -1 or base['title'].find('Just Cavalli') > -1 or base['title'].find('VIKTOR & ROLF') > -1 or base['title'].find('TED BAKER') > -1 or base['title'].find('Free People') > -1 or base['title'].find('Reclaimed Vintage') > -1 or base['title'].find('ASOS') > -1:
            pass
        else:
            csv_list.append(
                [title + base['title'].encode('CP932', 'ignore').decode('CP932').replace(u"\u2014", u"\u2015"),
                total_discription.replace(u"\u2014", u"\u2015"),
                str(int(base['price'].replace(u"\u2014", u"\u2015"))),
                "10",
                "1",
                "",
                base['size'].replace(u"\u2014", u"\u2015"),
                random.randint(5,10),
                base['image1'],
                base['image2'],
                base['image3'],
                base['image4'],
                base['image5']])

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

            df.to_csv("tops.csv", encoding="cp932", index=False)
