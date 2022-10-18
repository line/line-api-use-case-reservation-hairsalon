"""
UserSettingSample操作用モジュール

"""
import os
from datetime import datetime

from aws.dynamodb.base import DynamoDB
from dateutil.tz import gettz


class UserSetting(DynamoDB):  # ()内のクラスを継承する
    """UserSetting操作用クラス"""
    __slots__ = ['_table']  # インスタンス側で定義されたメンバ以外のメンバは持てなくなる

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("USER_SETTING_DB")
        super().__init__(table_name)
        # 基底クラスのメソッドを使って初期化：テーブル名のセットとdynamodbリソースの生成
        self._table = self._db.Table(table_name)

    def get_item(self, user_id):
        """
        データ取得

        Parameters
        ----------
        user_id : int
            ユーザーID

        Returns
        -------
        item : dict
            店舗情報

        """
        key = {'userId': user_id}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def put_item(self,user_id,profile_image_url):
        """
        データ登録

        Parameters
        ----------
        user_id : str
            ユーザーID
        profile_image_url : str
            プロフ画像URL

        Returns
        -------
        response : dict
            レスポンス情報

        """
        item ={
            'userId':user_id,
            'profile':{
                'profileImageUrl':profile_image_url
            },
            'updatedTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
        }
        try:
            response = self._put_item(item)
        except Exception as e:
            raise e
        return response

    def update_item(self,user_id,profile_image_url):
        key = {'userId':user_id}
        expression =('set profile=:profile, '
                      'updatedTime=:updated_time')
        expression_value = {
            ':profile': {'profileImageUrl':profile_image_url},
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
