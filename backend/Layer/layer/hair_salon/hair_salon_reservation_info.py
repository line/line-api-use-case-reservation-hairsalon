"""
HairSalonReservationInfo操作用モジュール

"""
import os
import uuid
from datetime import datetime
from dateutil.tz import gettz

from aws.dynamodb.base import DynamoDB
from common import utils


class HairSalonReservationInfo(DynamoDB):
    """HairSalonReservationInfo操作用クラス"""
    __slots__ = ['_table']

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("RESERVATION_INFO_DB")
        super().__init__(table_name)
        self._table = self._db.Table(table_name)

    def put_item(self, shop_id, shop_name, user_id, user_name,
                 course_id, course_name, staff_id, staff_name,
                 reservation_date, reservation_starttime,
                 reservation_endtime, amount):
        """
        データ登録

        Parameters
        ----------
        shop_id : int
            店舗ID
        shop_name : str
            店舗名
        user_id : str
            ユーザーID
        user_name : str
            ユーザー名
        course_id : int
            コースID
        course_name : str
            コース名
        staff_id : int
            スタッフID
        staff_name : str
            スタッフ名
        reservation_date : str
            予約日
        reservation_starttime : str
            予約開始時刻
        reservation_endtime : str
            予約終了時刻
        amount : int
            コースの値段

        Returns
        -------
        reservation_id :str
            予約ID

        """
        reservation_id = str(uuid.uuid4())
        item = {
            "reservationId": reservation_id,
            "shopId": shop_id,
            "shopName": shop_name,
            "userId": user_id,
            "userName": user_name,
            "courseId": course_id,
            "courseName": course_name,
            "staffId": staff_id,
            "staffName": staff_name,
            "reservationDate": reservation_date,
            "reservationStarttime": reservation_starttime,
            "reservationEndtime": reservation_endtime,
            "amount": amount,
            "expirationDate": utils.get_ttl_time(datetime.strptime(reservation_date, '%Y-%m-%d')),
            'createdTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
            'updatedTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
        }

        try:
            self._put_item(item)
        except Exception as e:
            raise e
        return reservation_id

    def delete_item(self, reservation_id):

        key = {'reservationId': reservation_id}
        try:
            response = self._delete_item(key)
        except Exception as e:
            raise e
        return response
