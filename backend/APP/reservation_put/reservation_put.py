import logging
import json
import os
import sys
from datetime import (datetime, timedelta)
from common import (common_const, utils, line)
from validation import hair_salon_param_check as validation
# DynamoDB操作クラスのインポート
from common.channel_access_token import ChannelAccessToken
from common.remind_message import RemindMessage
from hair_salon import hair_salon_utils
from hair_salon.hair_salon_shop_master import HairSalonShopMaster
from hair_salon.hair_salon_staff_reservation import HairSalonStaffReservation
from hair_salon.hair_salon_reservation_info import HairSalonReservationInfo

# 環境変数
REMIND_DATE_DIFFERENCE = int(os.getenv(
    'REMIND_DATE_DIFFERENCE'))
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
CHANNEL_TYPE = os.environ.get("CHANNEL_TYPE")
CHANNEL_ID = os.getenv('OA_CHANNEL_ID', None)
LIFF_CHANNEL_ID = os.getenv('LIFF_CHANNEL_ID', None)

# テーブル操作クラスの初期化
shop_master_table_controller = HairSalonShopMaster()
staff_reservation_table_controller = HairSalonStaffReservation()
reservation_info_table_controller = HairSalonReservationInfo()
channel_access_token_table_controller = ChannelAccessToken()
message_table_controller = RemindMessage()

# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
# LINEチャンネルチェック
if CHANNEL_ID is None:
    logger.error('Specify CHANNEL_ID as environment variable.')
    sys.exit(1)


def put_push_messages_to_dynamo(body, shop_info, remind_date_difference):
    """
    プッシュメッセージ情報を作成し、
    予約完了メッセージの送信とDynamoDBにメッセージを登録処理を実行する。

    Parameters
    ----------
    body : dict
        フロントから渡ってきたパラメータ
    remind_date_difference : int
        当日以前のリマインド行う日付の差分
        予約日以降のメッセージ送信を考慮し、マイナス値を許可（ex:3日前→ -3）

    Notes
    -----
    テンプレートメッセージでは後続メッセージのnotification_tokenを更新する必要がある。
    そのため、本メソッド中でも後続メッセージを先にDB投入し、後続メッセージのidを取得している。

    """
    # 予約確定通知メッセージの送信
    user_id = body['userId']
    shop_name = body['shopName']
    shop_address = shop_info['shop']['shopAddress']
    reservation_datetime = body['reservationDate'] + ' ' + \
        body['reservationStarttime'] + '-' + body['reservationEndtime']
    course_name = body['courseName']
    staff_name = body['staffName']
    flex = {'shop_name': shop_name,
            'shop_address': shop_address,
            'reservation_date': reservation_datetime,
            'course_name': course_name,
            'staff_name': staff_name,
            'remind_status': 'confirm'
            }
    flex_obj = hair_salon_utils.create_flex_message(**flex)
    # 短期チャネルアクセストークンの取得
    channel_info = channel_access_token_table_controller.get_item(
        CHANNEL_ID)
    logger.debug('message_channel_info: %s', channel_info)
    channel_access_token = channel_info['channelAccessToken']
    response = line.send_push_message(channel_access_token, flex_obj, user_id)
    logger.debug(response)
    # 当日送信するメッセージ情報をテーブル登録
    # 当日のリマインドデータを作成
    flex_on_day =  {'shop_name': shop_name,
                    'shop_address': shop_address,
                    'reservation_date': reservation_datetime,
                    'course_name': course_name,
                    'staff_name': staff_name,
                    'remind_status': 'on_day'
                    }
    flex_obj = hair_salon_utils.create_flex_message(**flex_on_day)
    remind_date_on_day = body['reservationDate']
    remind_message_id_on_day = message_table_controller.put_push_message(
        user_id, CHANNEL_ID, flex_obj, remind_date_on_day)

    # 当日より前のリマインドデータを作成
    date_text_before_day = str(abs(remind_date_difference))
    flex_before_day =  {'shop_name': shop_name,
                        'shop_address': shop_address,
                        'reservation_date': reservation_datetime,
                        'course_name': course_name,
                        'staff_name': staff_name,
                        'remind_status': 'day_before',
                        'day_before': date_text_before_day
                        }
    flex_obj = hair_salon_utils.create_flex_message(**flex_before_day)
    remind_date_before_day = utils.calculate_date_str_difference(
        body['reservationDate'], remind_date_difference)
    remind_message_id_on_day = message_table_controller.put_push_message(
        user_id, CHANNEL_ID, flex_obj, remind_date_before_day)


def interval_check(interval):
    """
    予約情報有無の判定処理
    インターバルがマイナス値の場合は既に予約あり

    Params
    -------
    interval:datetime.timedelta
        予約と予約の時差

    Returns
    -------
    boolean
        時差がマイナスの場合Trueを返す
    """
    if utils.timedelta_to_HM(interval) < 0:
        return True


def update_staff_reserved_db(body, shop_info):
    """
    スタッフ単位の予約情報を登録する

    Params
    -------
    body:dict
        フロントから送信されたパラメータ
    shop_info:dict
        予約店舗の情報

    Returns
    -------
    reservation_id:int
        採番された予約ID
    """
    shop_open_time = datetime.strptime(
        shop_info['shop']['openTime'], '%H:%M')
    shop_close_time = datetime.strptime(
        shop_info['shop']['closeTime'], '%H:%M')
    # 予約日のスタッフ状況テーブルを取得
    staff_reservation_info = staff_reservation_table_controller.get_item(
        body['staffId'], body['reservationDate'])
    if staff_reservation_info:
        # 該当日に予約データがある場合は、今回の予約開始終了時間も含めて最大予約可能時間幅を算出する
        push_item = {'reservedStartTime': body['reservationStarttime'],
                     'reservedEndTime': body['reservationEndtime']}
        staff_reservation_info['reservedTime'].append(push_item)
        # 予約データを開始時間で昇順にする
        reserved_time_list = sorted(staff_reservation_info['reservedTime'],
                                    key=lambda x: x['reservedStartTime'])
        logger.debug(reserved_time_list)
        list_length = len(reserved_time_list)
        max_interval = timedelta()
        for n in range(list_length):
            # 最初と最後の要素は営業時間との比較を行う
            if n == (list_length - 1):
                interval = shop_close_time - datetime.strptime(reserved_time_list[n]['reservedEndTime'], '%H:%M')  # noqa 501
            else:
                # 最後の要素でない場合のみ、次の要素の予約開始時間との比較を行う
                interval = datetime.strptime(reserved_time_list[n + 1]['reservedStartTime'], '%H:%M') - datetime.strptime(reserved_time_list[n]['reservedEndTime'], '%H:%M')  # noqa 501
            # 予約可否チェック
            if interval_check(interval):
                return True
            max_interval = interval if max_interval < interval else max_interval  # noqa 501

            if n == 0:
                interval = datetime.strptime(reserved_time_list[n]['reservedStartTime'], '%H:%M') - shop_open_time  # noqa 501
                if interval_check(interval):
                    return True
                max_interval = interval if max_interval < interval else max_interval  # noqa 501
        # 最大予約可能時間幅は分で登録する
        put_interval = utils.float_to_int(utils.timedelta_to_HM(max_interval))
        staff_reservation_table_controller.update_item(
            body['staffId'], body['reservationDate'],
            staff_reservation_info['reservedTime'], put_interval)
    else:
        # 該当日のデータが0件の場合は新規作成
        # 最大予約可能時間幅を算出
        before_interval = datetime.strptime(body['reservationStarttime'], '%H:%M') - shop_open_time  # noqa 501
        after_interval = shop_close_time - datetime.strptime(body['reservationEndtime'], '%H:%M')  # noqa 501
        max_interval = after_interval if before_interval < after_interval else before_interval  # noqa 501
        reservationDate = datetime.strptime(body['reservationDate'], '%Y-%m-%d')  # noqa 501
        # 最大予約可能時間幅は分で登録する
        put_interval = utils.float_to_int(utils.timedelta_to_HM(max_interval))
        staff_reservation_table_controller.put_item(
            body['staffId'],
            body['reservationDate'],
            put_interval,
            [{'reservedStartTime': body['reservationStarttime'],
              'reservedEndTime': body['reservationEndtime']}],
            str(reservationDate.year) + '-' + str(reservationDate.month)
        )

    return False


def put_reservation(body):
    """
    DyanmoDBに予約情報を登録する

    Params
    -------
    body:dict
        フロントから送信されたパラメータ

    Returns
    -------
    reservation_id:str
        予約登録時に採番された予約ID
    """
    # 予約情報の登録
    reservation_id = reservation_info_table_controller.put_item(
        body['shopId'], body['shopName'], body['userId'], body['userName'],
        body['courseId'], body['courseName'], body['staffId'],
        body['staffName'], body['reservationDate'],
        body['reservationStarttime'], body['reservationEndtime'],
        body['amount']
    )

    return reservation_id


def lambda_handler(event, context):
    """
    予約情報とメッセージ情報をDynamoDBに登録
    Params
    ----------
    event : dict
            フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    body : dict
        予約IDとクーポン情報
    """
    # パラメータログ、チェック
    logger.info(event)
    body = json.loads(event['body'])
    if body is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)
    #ユーザーID取得
    try:
        user_profile = line.get_profile(
            body['idToken'], LIFF_CHANNEL_ID)
        if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
            return utils.create_error_response('Forbidden', 403)
        else:
            body['userId'] = user_profile['sub']
    except Exception:
        logger.exception('不正なIDトークンが使用されています')
        return utils.create_error_response('Error')

    param_checker = validation.HairSalonParamCheck(body)  # noqa 501
    if error_msg := param_checker.check_api_reservation_put():
        error_msg_display = ('\n').join(error_msg)
        logger.error(error_msg_display)
        return utils.create_error_response(error_msg_display, 400)

    try:
        # 予約データ登録
        reservation_id = put_reservation(body)
        # 店舗情報の取得
        shop_info = shop_master_table_controller.get_item(body['shopId'])
        # スタッフごとの予約状況テーブルを更新する
        delete = update_staff_reserved_db(body, shop_info)
        # 該当時間に予約データが存在していた場合は予約データを削除する
        if delete:
            # 予約テーブルのデータを削除し、フロントに-1を返却する
            reservation_info_table_controller.delete_item(reservation_id)
            body = json.dumps({'reservationId': '-1'})
            return utils.create_success_response(body)
        # 予約完了メッセージの送信、前日リマインド、当日リマインド情報をDBに登録する
        put_push_messages_to_dynamo(
            body, shop_info, REMIND_DATE_DIFFERENCE)
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    body = json.dumps({'reservationId': reservation_id})
    return utils.create_success_response(body)
