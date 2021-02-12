import logging
import json
import requests
import json
from linebot import LineBotApi
from linebot.models import FlexSendMessage
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError)
from requests.models import Response

from common import common_const

# ログ出力の設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_push_message(channel_access_token, flex_obj, user_id):
    """
    プッシュメッセージ送信処理
    Parameters
    channel_access_token:str
        短期チャネルアクセストークン
    flex_obj:dict
        メッセージ情報
    user_id:str
        送信先のユーザーI
    Returns
    -------
    response:dict
        レスポンス情報
    """
    try:
        line_bot_api = LineBotApi(
            channel_access_token)
        # flexdictを生成する
        flex_obj = FlexSendMessage.new_from_json_dict(flex_obj)
        user_id = user_id
        response = line_bot_api.push_message(user_id, flex_obj)
    except LineBotApiError as e:
        logger.error(
            'Got exception from LINE Messaging API: %s\n' % e.message)
        for m in e.error.details:
            logger.error('  %s: %s' % (m.property, m.message))
        raise Exception
    except InvalidSignatureError as e:
        logger.error('Occur Exception: %s', e)
        raise Exception

    return response