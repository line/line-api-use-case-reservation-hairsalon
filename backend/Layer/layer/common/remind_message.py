"""
RemindMessage操作用モジュール

"""
from datetime import (datetime, timedelta)
from dateutil.tz import gettz
import uuid
import decimal
import os

from common import common_const
from aws.dynamodb.base import DynamoDB

ONE_WEEK = timedelta(days=7)
JST_UTC_TIMEDELTA = timedelta(hours=9)


class RemindMessage(DynamoDB):
    __slots__ = ['_table']

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("MESSAGE_DB")
        super().__init__(table_name)
        self._table = self._db.Table(table_name)

    def put_push_message(self, user_id, channel_id, flex_message,
                         remind_date):
        """
        プッシュメッセージを登録する

        Parameters
        ----------
        user_id : str
            ユーザーID
        channel_id : str
            メッセージ送信するチャネルのID
        flex_message : str
            フレックスメッセージのjson形式文字列
        remind_date : str
            リマインド日

        Returns
        -------
        response : dict
            レスポンス情報
        """
        message_id = str(uuid.uuid4())
        message_info = {
            'messageType': "push",
            'userId': user_id,
            'channelId': channel_id,
            'messageBody': flex_message
        }
        item = {
            'id': message_id,
            'messageInfo': message_info,
            'remindDate': remind_date,
            'expirationDate': self._get_timestamp_after_one_week(remind_date),
            'createdTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
            'updatedTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S")
        }

        try:
            response = self._put_item(item)
        except Exception as e:
            raise e
        return response


    def get_item(self, id):
        """
        idからアイテムを取得する

        Parameters
        ----------
        id : str
            メッセージのid

        Returns
        -------
        item : dict
            idから取得した1つのアイテム

        """
        key = {'id': id}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def query_index_remind_date(self, remind_date):
        """
        remindDateのindexからアイテムを取得する

        Parameters
        ----------
        remind_date : str
            リマインド日

        Returns
        -------
        items : list
            リマインド日から取得したアイテム

        """
        index = 'remindDate-index'
        expression = 'remindDate = :remindDate'
        expression_value = {
            ':remindDate': remind_date,
        }

        try:
            items = self._query_index(index, expression, expression_value)
        except Exception as e:
            raise e
        return items

    def _get_timestamp_after_one_week(self, date):
        """
        一週間後の日付のタイムスタンプを取得する。
        クラス内のみで使用。

        Parameters
        ----------
        date : str
            yyyy-MM-dd形式の日付文字列

        Returns
        -------
        after_one_week_date_timestamp: decimal
            指定日付の一週間後のタイムスタンプ
            DynamoDBに登録するためdecimal型としている
        """
        # データ削除期限日を指定
        after_one_week_date_utc = datetime.strptime(
            date, '%Y-%m-%d') + ONE_WEEK
        after_one_week_date_jst = after_one_week_date_utc - JST_UTC_TIMEDELTA
        # timestampはfloat型でDynamoDBに投入できないので変換
        after_one_week_date_timestamp = decimal.Decimal(
            after_one_week_date_jst.timestamp())
        return after_one_week_date_timestamp
