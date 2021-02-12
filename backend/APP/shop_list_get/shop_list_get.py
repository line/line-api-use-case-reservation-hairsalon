import logging
import json
import os
from common import utils
from hair_salon.hair_salon_shop_master import HairSalonShopMaster

# 環境変数
HAIR_SALON_M_SHOP_DB = os.environ.get("HAIR_SALON_M_SHOP_DB")
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# テーブル操作クラスの初期化
shop_master_table_controller = HairSalonShopMaster()


def create_area_shop_info(area_id, area_name, shop):
    """
    aria-shop形式で、一対多のdictを作成する。

    Parameters
    ----------
    area_id : int
        エリアID
    area_name : str
        地域名（関東・近畿等）
    shop : dict
        店舗情報

    Returns
    -------
    dict
        エリア-ショップ形式のデータ
    """
    return {
        'areaId': area_id,
        'areaName': area_name,
        'shop': [shop]
    }


def get_shop_list():
    """
    DBより取得した店舗一覧情報を返却する

    Returns
    -------
    area_shop_list:dict
        {カラム名: 値}のリスト
    """

    shop_list = shop_master_table_controller.scan()
    # フロントに返却する形式にデータ加工
    area_shop_dict = {}
    for shop in shop_list:
        areaId = shop['areaId']
        if areaId not in area_shop_dict:
            area_shop_dict[areaId] = create_area_shop_info(
                areaId, shop['areaName'], shop['shop'])
        else:
            area_shop_dict[areaId]['shop'].append(shop['shop'])

    area_shop_list = list(area_shop_dict.values())

    return area_shop_list


def lambda_handler(event, context):
    """
    店舗一覧情報を返す
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    shop_list : dict
        店舗一覧情報
    """
    # パラメータログ
    logger.info(event)
    try:
        shop_list = get_shop_list()
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    body = json.dumps(
        shop_list,
        default=utils.decimal_to_int, ensure_ascii=False)
    return utils.create_success_response(body)
