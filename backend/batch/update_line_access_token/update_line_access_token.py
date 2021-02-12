import os
import logging
import json
import requests
from datetime import (datetime, timedelta)
from dateutil.tz import gettz

from common import common_const as const
from common.channel_access_token import ChannelAccessToken

# 環境変数
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# テーブル操作クラスの初期化
channel_access_token_table_controller = ChannelAccessToken()


def update_limited_channel_access_token(channel_id, channel_access_token):  # noqa 501
    """
    指定のチャンネルIDの短期チャネルアクセストークンを更新する
    Parameters
    table : dynamoDB.Table
        dynamoDBのテーブルオブジェクト
    key :string
    itemDict : dict
        新規アイテム

    Returns
    -------
    なし
    """
    now = datetime.now(gettz('Asia/Tokyo'))
    # 取得から20日を期限とする
    limit_date = (now + timedelta(days=20)).strftime('%Y-%m-%d %H:%M:%S%z')

    channel_access_token_table_controller.update_item(channel_id,
                                                      channel_access_token,
                                                      limit_date)


def get_channel_access_token(channel_id, channel_secret):
    """
    MINIアプリの短期チャネルアクセストークンを新規で取得する

    Returns
    -------
    str
        access_token:短期のチャネルアクセストークン
    """

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'grant_type': 'client_credentials',
        'client_id': channel_id,
        'client_secret': channel_secret
    }

    response = requests.post(
        const.const.API_ACCESSTOKEN_URL,
        headers=headers,
        data=body
    )
    logger.debug('new_channel_access_token %s', response.text)
    res_body = json.loads(response.text)

    return res_body['access_token']


def lambda_handler(event, contexts):
    """
    dbの短期チャネルアクセストークンの期限をチェックし更新する

    Returns
    -------
    event
        channel_access_token:短期チャネルアクセストークン
    """
    channel_access_token_info = channel_access_token_table_controller.scan()
    for item in channel_access_token_info:
        # 途中処理でエラーが発生した場合でも後続処理が走るようにする
        try:
            if item.get('channelAccessToken'):
                limit_date = datetime.strptime(
                    item['limitDate'], '%Y-%m-%d %H:%M:%S%z')
                now = datetime.now(gettz('Asia/Tokyo'))
                # 本日以前の場合トークン再取得する
                if limit_date < now:
                    channel_access_token = get_channel_access_token(
                        item['channelId'], item['channelSecret'])
                    # DBのチャネルアクセストークンを更新
                    update_limited_channel_access_token(
                        item['channelId'], channel_access_token)
                    logger.info('channelId: %s updated', item['channelId'])
                else:
                    channel_access_token = item['channelAccessToken']  # noqa: E501
            # 1度もアクセストークン取得していない場合は新規取得する
            else:
                channel_access_token = get_channel_access_token(
                    item['channelId'], item['channelSecret'])
                update_limited_channel_access_token(
                    item['channelId'], channel_access_token)
                logger.info('channelId: %s created', item['channelId'])
        except Exception as e:
            logger.error('Occur Exception: %s', e)
            continue
