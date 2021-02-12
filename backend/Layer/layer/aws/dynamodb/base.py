"""
DynamoDB操作用基底モジュール

"""
import boto3
from boto3.dynamodb.conditions import Key
import logging
from datetime import (datetime, timedelta)

# ログ出力の設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DynamoDB:
    """DynamoDB操作用基底クラス"""
    __slots__ = ['_db', '_table_name']

    def __init__(self, table_name):
        """初期化メソッド"""
        self._table_name = table_name
        self._db = boto3.resource('dynamodb')

    def _put_item(self, item):
        """
        アイテムを登録する

        Parameters
        ----------
        item : dict
            登録するアイテム

        Returns
        -------
        response : dict
            レスポンス情報

        """
        try:
            response = self._table.put_item(
                Item=self._replace_data_for_dynamodb(item))
        except Exception as e:
            raise e

        return response

    def _update_item(self, key, expression, expression_value, return_value):
        """
        アイテムを更新する

        Parameters
        ----------
        key : dict
            更新するアイテムのキー
        expression : str
            更新の式
        expression_value : dict
            更新する値
        return_value : str
            responseで取得する値

        Returns
        -------
        response : dict
            レスポンス情報

        """
        try:
            response = self._table.update_item(Key=key,
                                               UpdateExpression=expression,
                                               ExpressionAttributeValues=self._replace_data_for_dynamodb(  # noqa: E501
                                                   expression_value),
                                               ReturnValues=return_value)
        except Exception as e:
            raise e

        return response

    def _update_item_optional(self, key, update_expression,
                              condition_expression, expression_attribute_names,
                              expression_value, return_value):
        """
        アイテムを更新する
        ※キー以外の更新条件がある場合に対応します
        ※

        Parameters
        ----------
        key : dict
            更新するアイテムのキー
        update_expression : str
            更新の式
        condition_expression : str
            更新条件
        expression_attribute_names:dict
            プレースホルダー
            （予約語に対応するため）
        expression_value : dict
            各変数宣言
        return_value : str
            responseで取得する値

        Returns
        -------
        response : dict
            レスポンス情報

        """
        try:
            response = self._table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ConditionExpression=condition_expression,
                ExpressionAttributeNames=expression_attribute_names,  # noqa 501
                ExpressionAttributeValues=self._replace_data_for_dynamodb(
                    expression_value),
                ReturnValues=return_value,
            )
        except Exception as e:
            raise e

        return response

    def _delete_item(self, key):
        """
        アイテムを削除する

        Parameters
        ----------
        key : dict
            削除するアイテムのキー

        Returns
        -------
        response : dict
            レスポンス情報

        """
        try:
            response = self._table.delete_item(Key=key)
        except Exception as e:
            raise e

        return response

    def _get_item(self, key):
        """
        アイテムを取得する

        Parameters
        ----------
        key : dict
            取得するアイテムのキー

        Returns
        -------
        response : dict
            レスポンス情報

        """
        try:
            response = self._table.get_item(Key=key)
        except Exception as e:
            raise e

        return response.get('Item', {})

    def _query(self, key, value):
        """
        queryメソッドを使用してアイテムを取得する

        Parameters
        ----------
        key : dict
            取得するアイテムのキー

        Returns
        -------
        items : list
            対象アイテムのリスト

        """
        try:
            response = self._table.query(
                KeyConditionExpression=Key(key).eq(value)
            )
        except Exception as e:
            raise e

        return response['Items']

    def _query_index(self, index, expression, expression_value):
        """
        indexからアイテムを取得する

        Parameters
        ----------
        index : str
            index名
        expression : str
            検索対象の式
        expression_value : dict
            expression内で使用する変数名と値

        Returns
        -------
        items : list
            検索結果

        """
        try:
            response = self._table.query(
                IndexName=index,
                KeyConditionExpression=expression,
                ExpressionAttributeValues=self._replace_data_for_dynamodb(
                    expression_value),
            )
        except Exception as e:
            raise e

        return response['Items']

    def _scan(self, key, value=None):
        """
        scanメソッドを使用してデータ取得

        Parameters
        ----------
        key : str
            キー名
        value : object, optional
            検索する値, by default None

        Returns
        -------
        items : list
            対象アイテムのリスト


        """
        scan_kwargs = {}
        if value:
            scan_kwargs['FilterExpression'] = Key(key).eq(value)

        try:
            response = self._table.scan(**scan_kwargs)
        except Exception as e:
            raise e

        return response['Items']

    def _get_table_size(self):
        """
        アイテム数を取得する

        Returns
        -------
        count : int
            テーブルのアイテム数

        """
        try:
            response = self._table.scan(Select='COUNT')
        except Exception as e:
            raise e

        return response.get('Count', 0)

    def _replace_data_for_dynamodb(self, value: dict):
        return value
