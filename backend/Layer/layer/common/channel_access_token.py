"""
ChannelAccessTokenテーブル操作用モジュール

"""
import os
from datetime import datetime
from dateutil.tz import gettz

from aws.dynamodb.base import DynamoDB


class ChannelAccessToken(DynamoDB):
    """ChannelAccessToken操作用クラス"""
    __slots__ = ['_table']

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get('CHANNEL_ACCESS_TOKEN_DB')
        super().__init__(table_name)
        self._table = self._db.Table(table_name)

    def get_item(self, channel_id):
        """
        channelIdからアイテムを取得する

        Parameters
        ----------
        channel_id : str
            チャネルID

        Returns
        -------
        item : dict
            チャネルの情報

        """
        key = {'channelId': channel_id}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def update_item(self, channel_id, channel_access_token, limit_date):
        """
        短期チャネルアクセストークンと期限日を更新する

        Parameters
        ----------
        channel_id : str
            LINE公式アカウント（Messageing API or MINIアプリ）のチャネルID
        channel_access_token :　str
            チャネルアクセストークン
        limit_date : str
            短期チャネルアクセストークンの期限日

        Returns
        -------
        response : dict
            レスポンス情報

        """
        key = {'channelId': channel_id}
        expression = "set channelAccessToken = :channel_access_token, \
            limitDate = :limit_date, updatedTime=:updated_time"
        expression_value = {
            ':channel_access_token': channel_access_token,
            ':limit_date': limit_date,
            ':updated_time': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S")
        }
        return_value = "UPDATED_NEW"

        try:
            response = self._update_item(key, expression,
                                         expression_value, return_value)
        except Exception as e:
            raise e
        return response

    def scan(self, channel_id=''):
        """
        scanメソッドを使用してデータ取得

        Parameters
        ----------
        channel_id : str
            LINE公式アカウント（Messageing API or MINIアプリ）のチャネルID

        Returns
        -------
        items : list
            取得したアイテムのリスト

        """

        key = 'channelId'

        try:
            items = self._scan(key, channel_id)
        except Exception as e:
            raise e
        return items
