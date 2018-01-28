import pymysql
import sys
import os
import codecs
import math

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
from polls.models import BaseProductCategoryList

import pandas as pd
import sys
from pprint import pprint

product_id_list = []
product_list = []
category_id1_list = []
category_id2_list = []
category_id3_list = []
category_id4_list = []

with codecs.open("item_category_20171231144014.csv", "r", "Shift-JIS", "ignore") as file:
    df = pd.read_table(file, delimiter=",")
    product_id_list = df['商品ID']
    product_list = df['商品名']
    category_id1_list = df['カテゴリID-1']
    category_id2_list = df['カテゴリID-2']
    category_id3_list = df['カテゴリID-3']
    category_id4_list = df['カテゴリID-4']

# baseのカテゴリーID
# 名前はバイマのcategory_name
# saki
# category_map = {
#     "アウター": 656022,
#     "ワンピース・オールインワン": 504924,
#     "トップス": 504926,
#     "ボトムス": 504927,
#     "ブライダル・パーティー": 746398,
# }

# watanabe bibi
# category_map = {
#     "ブライダル・パーティー": 832635,
#     "アウター": 832636,
# }

# shiori
# category_map = {
#     "ブライダル・パーティー": 835827,
#     "アウター": 835829,
#     "トップス": 835828,
# }

# mine
# category_map = {
#     "ブライダル・パーティー": 836365,
#     "アウター": 836366,
# }

# ikeda
category_map = {
    #     "ワンピース・オールインワン": 841126,
#     "ブライダル・パーティー": 841127,
#     "トップス": 841128,

}

# ikeda Reflet
# category_map = {
#     'ロングドレス': 848016,
#     'ミディアムドレス': 848017,
#     'ミニドレス': 848018,
#     'ワンピース': 848019,
#     'ジャケット': 848020,
#     'トップス': 848021,
#     'コート': 848026,
# }

# watanabe bibi
# category_map = {
#     "ブライダル・パーティー": 832635,
#     "アウター": 832636,
#     "トップス": 845716,
#     "ワンピース・オールインワン": 845719,
# }

# ikeda chartreuse
# category_map = {
#     "アウター": 819840,
#     "トップス": 819841,
#     "ブライダル・パーティー": 819839,
# }

# ikeda Minerva Sea
# category_map = {
#     "ワンピース・オールインワン": 792290,
#     "ブライダル・パーティー": 792289,
#     "トップス": 804755,
#     "アウター": 804756,
# }
# ikeda Silvia
# category_map = {
#     "ワンピース・オールインワン": 804605,
#     "ブライダル・パーティー": 804604,
#     "トップス": 804624,
#     "アウター": 804625,
# }
# category_map = {
#     "アウター": 743941,
#     "ワンピース・オールインワン": 750408,
#     "トップス": 750405,
#     "ボトムス": 750406,
#     "ブライダル・パーティー": 779338,
# }
with transaction.atomic():
    for i, product in enumerate(product_id_list):
        product_dict = {
            "base_product_id":None,
            "product_name":"",
            "category_id1":None,
            "category_id2":None,
            "category_id3":None,
            "category_id4":None,
        }
        # 大特価新作の文言を抜いたタイトルでバイマから検索
        # ikeda
        buyma_product = BaseFromAPI.objects.filter(title=product_list[i]).values().first()

        # buyma_product = BaseFromAPI.objects.filter(title=product_list[i].replace('「大特価」', '').replace('☆SALE☆ ', '').replace('「破格」 ', '')).values().first()
        # saki
        # buyma_product = Buyma.objects.filter(title=product_list[i].replace('大特価 新作 ', '')).values().first()
        if buyma_product is None and math.isnan(category_id1_list[i]) == True:
            pass
        else:
            if False == math.isnan(category_id1_list[i]):
                # product_dict['category_id1'] = category_id1_list[i]
                pass
            else:
                product_dict['base_product_id'] = product_id_list[i]
                product_dict['product_name'] = product_list[i]
                product_dict['category_id1'] = category_map[buyma_product['category_1']]
                product_dict['category_id2'] = category_id2 = None if True == math.isnan(category_id2_list[i]) else int(category_id2_list[i])
                product_dict['category_id3'] = category_id3 = None if True == math.isnan(category_id3_list[i]) else int(category_id3_list[i])
                product_dict['category_id4'] = category_id4 = None if True == math.isnan(category_id4_list[i]) else int(category_id4_list[i])

                BaseProductCategoryList.objects.create(**product_dict)
