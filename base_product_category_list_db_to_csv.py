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
from polls.models import Buyma
from polls.models import BaseProductCategoryList

import pandas as pd
from pprint import pprint

base_product_category_list = BaseProductCategoryList.objects.values()
csv_list = []
i = 0
for base_product_category in base_product_category_list:
    csv_list.append([base_product_category['base_product_id'],
                     base_product_category['product_name'],
                     base_product_category['category_id1'],
                     base_product_category['category_id2'],
                     base_product_category['category_id3'],
                     base_product_category['category_id4']])
    i += 1

df = pd.DataFrame(
    csv_list,
    columns=[
        '商品ID',
        '商品名',
        'カテゴリID-1',
        'カテゴリID-2',
        'カテゴリID-3',
        'カテゴリID-4',
    ])

df.to_csv("base_product_category_list.csv", encoding="shift_jis")
