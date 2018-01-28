import pymysql
import sys
import os
import pprint
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

title = "大特価 新作 "

discription1 = """===こちらは取寄せ商品になります。

１２～１８日ほどお時間を頂きます。===


★ご購入前にこちら

https://lilywhite.thebase.in/about

ご確認をお願い致します★

""".encode('CP932').decode('SJIS')

discription2 = """※お客様ご使用のPC環境により商品画像のカラーが多少異なる場合があります。
仕入時期により多少デザインなど異なる場合があります。ご了承ください。

※サイズは人の手によって測っているため、
1-3cmの誤差がある場合がございますので、予めご了承くださいませ。



海外倉庫からの発送の為、到着が１２〜１８日ほどかかる事、
ご了承下さいませ。
（状況によっては更にかかる場合がございますので
余裕をもったご注文をお願いいたします）

モニター環境により若干色誤差が出ます。
実物とは色合いが異なって見える場合もございますが、
不良品ではないためご対応出来かねます。

自社スタッフによる徹底検品を行っておりますが、
海外製品の為、裁縫が荒い部分があるかもしれませんが
ご了承くださいませ。
細かい所まで気にされる神経質な方はご落札をご遠慮下さい。

サイズ表記は平置きの為、多少の誤差がでる事がございます。

イメージ、サイズ違いでの返品、交換は基本的にお受けできかねます。""".encode('CP932', 'ignore').decode('CP932')

category_name = "アウター"
shop_name = 1075706
# buyma_list = Buyma.objects.filter(is_csv=0).filter(shop_name=shop_name, category_name=category_name).order_by('title').order_by('image1')[:2000].values()
buyma_list = Buyma.objects.filter(is_csv=0).filter(shop_name=shop_name, category_name=category_name).order_by('title').order_by('image1').values()
csv_list = []
previous_title = ""

with transaction.atomic():
    # i = 0
    for buyma in buyma_list:
        # update_buyma = Buyma.objects.filter(id=buyma['id']).first()
        # update_buyma.is_csv = 1
        # update_buyma.save()
        total_discription = ""
        total_discription += discription1
        if buyma['discription2'] is not None:
            total_discription += str(buyma['discription2']) + '\n'
        if buyma['discription1'] is not None:
            total_discription += str(buyma['discription1'])
        total_discription += discription2

        if buyma['title'].find('Chicwish') > -1 or buyma['title'].find('Little Mistress') > -1 or buyma['title'].find('Chi Chi London') > -1 or buyma['title'].find('Lipsy') > -1:
            pass
        else:
            # current_title = buyma['title']
            # if previous_title != current_title:
            #     i += 1
            # previous_title = buyma['title']
            csv_list.append(
                [title + buyma['title'].encode('CP932', 'ignore').decode('CP932'),
                total_discription,
                str(int(buyma['price'])),
                "10",
                "1",
                "",
                buyma['size'],
                "10",
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

            df.to_csv("outer.csv", encoding="cp932", index=False)
