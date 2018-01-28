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
from datetime import datetime

title = ""

discription1 = """-------こちらは取寄せ商品になります。

１２～１８日ほどお時間を頂きます。--------


""".encode('CP932').decode('SJIS')

discription2 = """※お客様ご使用のPC環境により商品画像のカラーが多少異なる場合があります。
仕入時期により多少デザインなど異なる場合があります。ご了承ください。

※サイズは人の手によって測っているため、
1-3cmの誤差がある場合がございますので、予めご了承くださいませ。


海外倉庫からの発送の為、到着が１２〜１８日ほどかかる事、
ご了承下さい。
（状況によっては更にかかる場合がございますので
到着日に余裕を持たせてご注文をお願いいたします）

自社スタッフによる徹底検品を行っておりますが、
海外製品の為、裁縫が荒い部分があるかもしれませんが
ご了承くださいませ。
細かい所まで気にされる神経質な方はご落札をご遠慮下さい。

""".encode('CP932', 'ignore').decode('CP932')

category_name = "アウター"
shop_name = 1075706
# buyma_list = Buyma.objects.filter(is_csv=0).filter(shop_name=shop_name, category_name=category_name).order_by('title').order_by('image1')[:2000].values()
buyma_list = Buyma.objects.filter(is_csv=0).filter(shop_name=shop_name, category_name=category_name).order_by('title').order_by('image1').values()
csv_list = []
previous_title = ""

with transaction.atomic():
    data_id = 1
    adm_id = 1
    for buyma in buyma_list:
        if buyma['category_name'] == 'ブライダル・パーティー':
            B_categ_ID = 510911 #パーティードレス
            keyword = 'ドレス:ロングドレス:ミニドレス:ミディアムドレス'
        else if buyma['category_name'] == 'ワンピース・オールインワン':
            B_categ_ID = 511101 #その他ワンピース
            keyword = 'ワンピース:オールインワン'

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
            csv_list.append([
                # ◎新規出品・更新時に必須
                # ◯更新時に必須
                'e-' + data_id, #Code ◎
                B_categ_ID, #BCategID ◯
                buyma['title'] + ' 大特価 新作', #KtaiTitle ◯
                buyma['price'], #KtaiPrice ◯
                total_discription, #KtaiCaption ◯
                'CBMrtsP', #KtaiDealType ◯
                'CBPhi', #KtaiChargeType
                '', #AdmID
                random.randint(5,10), #StockNum 在庫数
                keyword, #Keyword
                '', #KtaiUserRate
                '画像1', #KtaiImageLinkName1
                'U', #KtaiImageType1 U:画像保管庫のURL
                '', #KtaiImageURL1
                '画像2', #KtaiImageLinkName2
                'U', #KtaiImageType2
                '', #KtaiImageURL2
                '画像3', #KtaiImageLinkName3
                'U', #KtaiImageType3
                '', #KtaiImageURL3
                '画像4', #KtaiImageLinkName4
                'U', #KtaiImageType4
                '', #KtaiImageURL4
                '画像5', #KtaiImageLinkName5
                '', #KtaiImageType5
                '', #KtaiImageURL5
                '', #KtaiImageLinkName6
                '', #KtaiImageType6
                '', #KtaiImageURL6
                '', #KtaiImageLinkName7
                '', #KtaiImageType7
                '', #KtaiImageURL7
                '', #KtaiImageLinkName8
                '', #KtaiImageType8
                '', #KtaiImageURL8
                '', #KtaiImageLinkName9
                '', #KtaiImageType9
                '', #KtaiImageURL9
                '', #KtaiImageLinkName10
                '', #KtaiImageType10
                '', #KtaiImageURL10
                'B', #ShipFeeType 送料別B
                750, #ShipFee 送料
                '', #DeliveryType メール便対応なし
                '10000円以上の商品は送料無料になります。', #KtaiShipComment 送料コメント
                '振込先はメールでご案内いたします。', #KtaiDealComment
                '', #KtaiPriceLabel1
                '', #KtaiPriceLabel2
                '', #KtaiCaptionPC
                '', #KtaiCaptionSP
                '', #KtaiDetailLinkName
                '', #KtaiDetailComment
                '', #Option1
                '', #Option2
                '', #Option3
                '', #Option4
                '', #Option5
                datetime.now().strftime("%Y/%m/%d"), #SalesStartDate
                '', #StartDate
                'O', #ExhibitStatus 販売ステータス O:出品中
                '', #AdmTitle
                '', #JanCode
                '', #IsbnCode
                '', #NameModel
                '', #SecretPagePassword
                '', #SecretPageTitle
                '', #SecretPageMessage
                '', #StockShow
                '完売しました！', #KtaiNoStockMessage
                '', #KtaiSpecLinkName
                '', #KtaiSpec1
                '', #KtaiSpec2
                '', #KtaiSpec3
                '', #KtaiSpec4
                '', #KtaiSpec5
                '', #MaxBuyNum
                '', #KtaiStockShowStartNum
                '', #KtaiStockMessage1
                '', #KtaiStockMessage2
                'I ', #Tax I:内税
                'MX' #exhibittype Wowma!・Wowma! for au（ケータイ版）◎

                # [title + buyma['title'].encode('CP932', 'ignore').decode('CP932'),
                # total_discription,
                # str(int(buyma['price'])),
                # "10",
                # "1",
                # "",
                # buyma['size'],
                # random.randint(5,10),
                # buyma['image1'],
                # buyma['image2'],
                # buyma['image3'],
                # buyma['image4'],
                # buyma['image5']
            ])

            df = pd.DataFrame(
                csv_list,
                columns=[
                    'Code',
                    'BCategID',
                    'KtaiTitle',
                    'KtaiPrice',
                    'KtaiCaption',
                    'KtaiDealType',
                    'KtaiChargeType',
                    'AdmID',
                    'StockNum',
                    'Keyword',
                    'KtaiUserRate',
                    'KtaiImageLinkName1',
                    'KtaiImageType1',
                    'KtaiImageURL1',
                    'KtaiImageLinkName2',
                    'KtaiImageType2',
                    'KtaiImageURL2',
                    'KtaiImageLinkName3',
                    'KtaiImageType3',
                    'KtaiImageURL3',
                    'KtaiImageLinkName4',
                    'KtaiImageType4',
                    'KtaiImageURL4',
                    'KtaiImageLinkName5',
                    'KtaiImageType5',
                    'KtaiImageURL5',
                    'KtaiImageLinkName6',
                    'KtaiImageType6',
                    'KtaiImageURL6',
                    'KtaiImageLinkName7',
                    'KtaiImageType7',
                    'KtaiImageURL7',
                    'KtaiImageLinkName8',
                    'KtaiImageType8',
                    'KtaiImageURL8',
                    'KtaiImageLinkName9',
                    'KtaiImageType9',
                    'KtaiImageURL9',
                    'KtaiImageLinkName10',
                    'KtaiImageType10',
                    'KtaiImageURL10',
                    'ShipFeeType',
                    'ShipFee',
                    'DeliveryType',
                    'KtaiShipComment',
                    'KtaiDealComment',
                    'KtaiPriceLabel1',
                    'KtaiPriceLabel2',
                    'KtaiCaptionPC',
                    'KtaiCaptionSP',
                    'KtaiDetailLinkName',
                    'KtaiDetailComment',
                    'Option1',
                    'Option2',
                    'Option3',
                    'Option4',
                    'Option5',
                    'SalesStartDate',
                    'StartDate',
                    'ExhibitStatus',
                    'AdmTitle',
                    'JanCode',
                    'IsbnCode',
                    'NameModel',
                    'SecretPagePassword',
                    'SecretPageTitle',
                    'SecretPageMessage',
                    'StockShow',
                    'KtaiNoStockMessage',
                    'KtaiSpecLinkName',
                    'KtaiSpec1',
                    'KtaiSpec2',
                    'KtaiSpec3',
                    'KtaiSpec4',
                    'KtaiSpec5',
                    'MaxBuyNum',
                    'KtaiStockShowStartNum',
                    'KtaiStockMessage1',
                    'KtaiStockMessage2',
                    'Tax',
                    'exhibittype',
                ])

                data_id += 1

            df.to_csv("outer.csv", encoding="cp932", index=False)
