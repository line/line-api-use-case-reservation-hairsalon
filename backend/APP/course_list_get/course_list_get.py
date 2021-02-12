import logging
import json
import os
from common import (common_const, utils)
from hair_salon.hair_salon_shop_master import HairSalonShopMaster
from validation import hair_salon_param_check as validation

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


def lambda_handler(event, context):
    """
    コース一覧情報を返す
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    course_list : dict
        コース情報
    """
    # パラメータログ、チェック
    logger.info(event)
    req_param = event['queryStringParameters']
    if req_param is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)

    param_checker = validation.HairSalonParamCheck(req_param)  # noqa 501
    if error_msg := param_checker.check_api_course_list_get():
        error_msg_display = ('\n').join(error_msg)
        logger.error(error_msg_display)
        return utils.create_error_response(error_msg_display, 400)

    try:
        # 店舗IDをキーにデータ取得
        course_list = shop_master_table_controller.get_item(
            int(req_param['shopId']))
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    body = json.dumps(
        course_list['course'],
        default=utils.decimal_to_int, ensure_ascii=False)
    return utils.create_success_response(body)
