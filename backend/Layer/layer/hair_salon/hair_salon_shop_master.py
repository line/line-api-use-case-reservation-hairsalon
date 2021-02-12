"""
HairSalonShopMasterSample操作用モジュール

"""
import os
from aws.dynamodb.base import DynamoDB


class HairSalonShopMaster(DynamoDB):  # ()内のクラスを継承する
    """HairSalonShopMaster操作用クラス"""
    __slots__ = ['_table']  # インスタンス側で定義されたメンバ以外のメンバは持てなくなる

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("SHOP_MASTER_DB")
        super().__init__(table_name)
        # 基底クラスのメソッドを使って初期化：テーブル名のセットとdynamodbリソースの生成
        self._table = self._db.Table(table_name)

    def get_item(self, shop_id):
        """
        データ取得

        Parameters
        ----------
        shop_id : int
            店舗ID

        Returns
        -------
        item : dict
            店舗情報

        """
        key = {'shopId': shop_id}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def scan(self):
        """
        scanメソッドを使用してデータ取得

        Parameters
        ----------
        なし

        Returns
        -------
        items : list
            店舗情報のリスト

        """
        key = 'shop_id'

        try:
            items = self._scan(key)
        except Exception as e:
            raise e
        return items
