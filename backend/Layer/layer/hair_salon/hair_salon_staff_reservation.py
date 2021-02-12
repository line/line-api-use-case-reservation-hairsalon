"""
HairSalonStaffReservation操作用モジュール

"""
import os
from datetime import datetime
from dateutil.tz import gettz

from aws.dynamodb.base import DynamoDB
from common import utils


class HairSalonStaffReservation(DynamoDB):
    """HairSalonStaffReservation操作用クラス"""
    __slots__ = ['_table']

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("STAFF_RESERVATION_INFO_DB")
        super().__init__(table_name)
        self._table = self._db.Table(table_name)

    def put_item(self, staff_id, reserved_day, reservable_time_term,
                 reserved_time, reserved_year_month):
        """
        データ登録

        Parameters
        ----------
        staff_id : int
            スタッフID
        reserved_day : str
            予約日
        reservable_time_term : int
            予約可能最長時間
        reserved_time: dict
            予約開始終了時間情報
        reserved_year_month : str
            予約年月

        Returns
        -------
        response : dict
            レスポンス情報

        """
        item = {
            'staffId': staff_id,
            'reservedDay': reserved_day,
            'reservedYearMonth': reserved_year_month,
            'reservedTime': reserved_time,
            'reservableTimeTerm': reservable_time_term,
            "expirationDate": utils.get_ttl_time(datetime.strptime(reserved_day, '%Y-%m-%d')),
            'createdTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
            'updatedTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
        }

        try:
            response = self._put_item(item)
        except Exception as e:
            raise e
        return response

    def update_item(self, staff_id, reserved_day,
                    reserved_time, reservable_time_term):
        """
        データ更新

        Parameters
        ----------
        staff_id : int
            店舗ID
        reserved_day : str
            予約日
        reserved_time: dict
            予約開始終了時間情報
        reservable_time_term : int
            予約可能最長時間

        Returns
        -------
        response : dict
            レスポンス情報

        """
        key = {'staffId': staff_id, 'reservedDay': reserved_day}
        expression = ('set reservableTimeTerm=:reservable_time_term, '
                      'reservedTime=:reserved_time, '
                      'updatedTime=:updated_time')
        expression_value = {
            ':reservable_time_term': reservable_time_term,
            ':reserved_time': reserved_time,
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

    def get_item(self, staff_id, reserved_day):
        """
        データ取得

        Parameters
        ----------
        staff_id : int
            スタッフID
        reserved_day : str
            予約日

        Returns
        -------
        item : dict
            特定日の予約情報

        """
        key = {'staffId': staff_id, 'reservedDay': reserved_day}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def query_index_staff_id_reserved_year_month(self, staff_id, reserved_year_month):  # noqa: E501
        """
        queryメソッドを使用してstaffId-reservedYearMonth-indexのインデックスからデータ取得

        Parameters
        ----------
        staff_id : int
            スタッフID
        reserved_year_month : str
            予約年月

        Returns
        -------
        items : list
            特定年月の予約情報のリスト

        """
        index = 'staffId-reservedYearMonth-index'
        expression = 'staffId = :staff_id AND reservedYearMonth = :reserved_year_month'  # noqa: E501
        expression_value = {
            ':staff_id': staff_id,
            ':reserved_year_month': reserved_year_month
        }

        try:
            items = self._query_index(index, expression, expression_value)
        except Exception as e:
            raise e
        return items
