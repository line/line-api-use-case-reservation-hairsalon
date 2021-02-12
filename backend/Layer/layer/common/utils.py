"""
共通関数
"""
from decimal import Decimal
from datetime import (datetime, timedelta)
import decimal
import os

from common import common_const


def create_response(status_code, body):
    """
    フロントに返却するデータを作成する

    Parameters
    ----------
    status_code : int
        フロントに返却するステータスコード
    body:dict,str
        フロントに返却するbodyに格納するデータ
    Returns
    -------
    response : dict
        フロントに返却するデータ
    """
    response = {
        'statusCode': status_code,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': body
    }
    return response


def create_error_response(body, status=500):
    """
    エラー発生時にフロントに返却するデータを作成する

    Parameters
    ----------
    body : dict,str
        フロントに返却するbodyに格納するデータ
    status:int
        フロントに返却するステータスコード
    Returns
    -------
    create_response:dict
        フロントに返却するデータ
    """
    return create_response(status, body)


def create_success_response(body):
    """
    正常終了時にフロントに返却するデータを作成する

    Parameters
    ----------
    body : dict,str
        フロントに返却するbodyに格納するデータ
    Returns
    -------
    create_response:dict
        フロントに返却するデータ
    """
    return create_response(200, body)


def separate_comma(num):
    """
    数値を3桁毎のカンマ区切りにする

    Parameters
    ----------
    num : int
        カンマ区切りにする数値

    Returns
    -------
    result : str
        カンマ区切りにした文字列
    """
    return '{:,}'.format(num)


def decimal_to_int(obj):
    """
    Decimal型をint型に変換する。
    json形式に変換する際にDecimal型でエラーが出るため作成。
    主にDynamoDBの数値データに対して使用する。

    Parameters
    ----------
    obj : obj
        Decimal型の可能性があるオブジェクト

    Returns
    -------
    int, other
        Decimal型の場合int型で返す。
        その他の型の場合そのまま返す。
    """
    if isinstance(obj, Decimal):
        return int(obj)


def float_to_int(obj):
    """
    float型をint型に変換する。
    DynamoDB登録時にfloat型でエラーが出るため作成。

    Parameters
    ----------
    obj : obj
        float型の可能性があるオブジェクト

    Returns
    -------
    int, other
        float型の場合int型で返す。
        その他の型の場合そのまま返す。
    """
    if isinstance(obj, float):
        return int(obj)


def format_date(date, before_format, after_format):
    """
    指定されたstr型の日付データのフォーマットを変換し、str型で返す
    Parameters
    date:str
        フォーマット変換したいstr型の日付データ
    before_format:str
        変換前の日付フォーマット
    after_format:str
        変換した日付フォーマット
    Returns
    -------
    date
        生成したID
    """
    before_date = datetime.strptime(date, before_format)
    formated_date = before_date.strftime(after_format)

    return formated_date


def get_time_interval(time1, time2):
    """
    時間間隔を算出する
    Parameters
    time1:str
        フォーマット変換したいstr型の日付データ
    time2:str
        変換前の日付フォーマット
    Returns
    -------
    interval:datetime.timedelta
        算出した時間差
    """
    datetime.strptime(time1, '%H:%M')
    interval = time1 - time2

    return interval


def timedelta_to_HM(td):
    """
    timedelta型のデータをminutesに変換
    Parameters
    td:timedelta
        変換したいデータ
    Returns
    -------
    date
        生成したID
    """
    sec = td.total_seconds()
    hours = sec//3600 * 60
    minutes = sec % 3600//60

    return hours + minutes


def calculate_date_str_difference(date_str, date_difference):
    """
    日付文字列と差分の日数を元に、日付計算を行う

    Parameters
    ----------
    date_str : str
        yyyy-MM-dd形式の日付
    date_difference : int
        日付の差分
        引き算の場合はマイナス値

    Returns
    -------
    result_date_str : str
        計算後のyyyy-MM-dd形式の日付
    """
    target_date = datetime.strptime(date_str, '%Y-%m-%d')
    date_timedelta = timedelta(days=date_difference)
    result_date = target_date + date_timedelta
    result_date_str = datetime.strftime(result_date, '%Y-%m-%d')
    return result_date_str


def get_timestamp_after_one_week(date):
    """
    一週間後の日付のタイムスタンプを取得する。

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
        date, '%Y-%m-%d') + common_const.const.ONE_WEEK
    after_one_week_date_jst = after_one_week_date_utc - \
        common_const.const.JST_UTC_TIMEDELTA
    # timestampはfloat型でDynamoDBに投入できないので変換
    after_one_week_date_timestamp = decimal.Decimal(
        after_one_week_date_jst.timestamp())
    return after_one_week_date_timestamp


def get_ttl_time(param_datetime):
    """
    DynamoDBのTimeToLive時間を返却
    Parameters
    -------
    param_datetime:  datetime
        ttlを設定する基準となる日
    Returns
    -------
    delete_unixtime : int
        データ削除するUNIX時間

    """
    delete_day = int(os.getenv('TTL_DAY', None))
    delete_date_time = param_datetime + timedelta(days=delete_day)
    delete_unixtime = int(delete_date_time.timestamp())
    return delete_unixtime