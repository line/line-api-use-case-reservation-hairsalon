import logging
import json
import os
from common import (common_const, utils)
from validation import hair_salon_param_check as validation
from hair_salon.hair_salon_staff_reservation import HairSalonStaffReservation

# 環境変数
HAIR_SALON_STAFF_RESERVATION_DB = os.environ.get("HAIR_SALON_STAFF_RESERVATION_DB")  # noqa 501
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# テーブル操作クラスの初期化
staff_reservation_table_controller = HairSalonStaffReservation()


def get_reserved_time(params):
    """
    指定のstaffIdとpreferredDayをもとに該当スタッフの予約状況データを取得する
    Parameters
    -------
    params:dict
        フロントより取得したパラメータ
    Returns
    -------
    reserved_time_list:dict
        予約済み時間リスト
    """
    # DBよりstaffIdとpreferredDayをもとにスタッフの予約済み時間を取得する
    reserved_time_list = staff_reservation_table_controller.get_item(
        int(params['staffId']), params['preferredDay'])
    if reserved_time_list:
        # 返却データ形式に整形
        reserved_time_list['reservedInfo'] = reserved_time_list['reservedTime']
        del reserved_time_list['reservedTime']

    return reserved_time_list


def lambda_handler(event, context):
    """
    予約済み時間情報を返す
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    reserved_time_list : dict
        予約済み時間情報
    """
    # パラメータログ、チェック
    logger.info(event)
    req_param = event['queryStringParameters']
    if req_param is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)

    param_checker = validation.HairSalonParamCheck(req_param)  # noqa 501
    if error_msg := param_checker.check_api_reserved_time_get():
        error_msg_display = ('\n').join(error_msg)
        logger.error(error_msg_display)
        return utils.create_error_response(error_msg_display, 400)

    try:
        # スタッフIDと希望日時から予約済み時間情報を取得する
        reserved_time_list = get_reserved_time(req_param)
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    body = json.dumps(
        reserved_time_list,
        default=utils.decimal_to_int, ensure_ascii=False)
    return utils.create_success_response(body)
