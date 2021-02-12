import logging
import datetime
from dateutil.tz import gettz
import os
import boto3
import json

from common import (line, utils)
from hair_salon import hair_salon_utils
# DynamoDB操作クラスのインポート
from common.remind_message import RemindMessage
from common.channel_access_token import ChannelAccessToken


# ログ出力の設定
logger = logging.getLogger()
LOGGER_LEVEL = os.getenv('LOGGER_LEVEL', None)
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# テーブルの宣言
remind_message_table_controller = RemindMessage()
channel_access_token_table_controller = ChannelAccessToken()


def send_message_from_dynamodb():
    """
    テーブルに登録されたデータを取得し、プッシュメッセージ送信を行う。
    """

    # 本日送信のメッセージをDynamoテーブルから取得する
    today = datetime.datetime.strftime(
        (datetime.datetime.now(gettz('Asia/Tokyo')).date()), '%Y-%m-%d')

    today_messages = remind_message_table_controller.query_index_remind_date(
        today)

    # NOTE: [queryの検索]データが0件→Items有り [get_itemの検索]データが0件→ItemsというKey自体無し
    if not today_messages:
        return

    # MEMO: Lambdaの実行時間が長くなる場合、SQSに一度保存した後に他Lambdaでポーリングさせることを考える。
    # MEMO: 上の場合 (EventBridge→Lambda→SQS→Lambda)
    for message_item in today_messages:
        # Decimal型をintに変換
        message_info = json.loads(json.dumps(
            message_item['messageInfo'],
            default=utils.decimal_to_int))
        try:
            channel_info = channel_access_token_table_controller.get_item(
                message_info['channelId'])
            line.send_push_message(channel_info['channelAccessToken'],
                                   message_info['messageBody'],
                                   message_info['userId'])
        except Exception as e:
            logger.exception(
                'プッシュメッセージ送信でエラーが発生しました。該当メッセージを確認してください。メッセージID：%s',
                message_item['id'])
            logger.exception('エラー内容: %s', e)
            continue


def lambda_handler(event, context):
    """
    Webhookに送信されたLINEトーク内容を返却する

    Parameters
    ----------
    event : dict
        Webhookへのリクエスト内容。
    context : dict
        コンテキスト内容。

    Returns
    -------
    Response : dict
        Webhookへのレスポンス内容。
    """
    logger.info(event)

    try:
        send_message_from_dynamodb()
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('ERROR')

    return utils.create_success_response('OK')
