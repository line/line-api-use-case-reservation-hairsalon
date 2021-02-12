import logging
import json
import os
from datetime import datetime
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


def get_staff_calendar(params):
    """
    DBよりスタッフの予約情報を取得し、日毎に空きがあるか判定し、結果を返す
    Params
    -------
    params:dict
        フロントからのパラメータ群
    Returns
    -------
    return_calendar:dict
        {カラム名: 値}のリスト
    """
    # 指定したスタッフIDの希望月の空き情報をDBより取得する
    staff_calendar = staff_reservation_table_controller.query_index_staff_id_reserved_year_month(  # noqa501
        int(params['staffId']), params['preferredYearMonth']
    )
    course_minutes = int(params['courseMinutes'])
    # カレンダーは希望月内のデータのみ返却する
    return_calendar = {'calendarYearMonth': params['preferredYearMonth']}
    return_calendar['calendarDays'] = []
    for staff_reservation_info in staff_calendar:
        # 予約コースの施術時間が担当スタッフの最大空き時間以内かチェック
        reservable_time_term = int(
            staff_reservation_info['reservableTimeTerm'])
        if reservable_time_term < course_minutes:
            vacancy_flg = 0
        else:
            vacancy_flg = 1
        reserved_day = datetime.strptime(
            staff_reservation_info['reservedDay'], '%Y-%m-%d')
        return_day = reserved_day.day
        return_calendar['calendarDays'].append({'day': int(return_day),
                                                'vacancyFlg': vacancy_flg})
    return return_calendar


def lambda_handler(event, context):
    """
    スタッフの日毎の空き情報を返却する
    Parameters
    ----------
    event : dict
        フロントからのパラメータ群
    context : dict
        コンテキスト内容。
    Returns
    -------
    return_calendar : dict
        スタッフの日毎の空き情報（予約がある日のみ空き有無の判定結果を返す）
    """
    # パラメータログ、チェック
    logger.info(event)
    req_param = event['queryStringParameters']
    if req_param is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)

    param_checker = validation.HairSalonParamCheck(req_param)  # noqa 501
    if error_msg := param_checker.check_api_staff_calendar_get():
        error_msg_display = ('\n').join(error_msg)
        logger.error(error_msg_display)
        return utils.create_error_response(error_msg_display, 400)

    try:
        # スタッフIDで希望月のスタッフの空き情報を取得する
        staff_calendar = get_staff_calendar(req_param)
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    body = json.dumps(
        staff_calendar,
        default=utils.decimal_to_int,
        ensure_ascii=False)
    return utils.create_success_response(body)
