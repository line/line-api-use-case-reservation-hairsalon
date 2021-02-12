
import datetime


class ParamCheck():
    """
    パラメータチェックを実施するクラス。
    """

    def __init__(self):
        """
        初期化を実施する。
        """
        pass

    def check_required(self, columns, column_name):
        """
        必須チェックを実施する。

        Parameters
        ----------
        columns : obj
            必須チェックをする項目
        column_name: str
            項目名

        Returns
        -------
        str
            エラー内容
        """
        columns_replaced = str(columns).replace(' ', '')

        if columns is None or not columns_replaced:
            return '必須入力エラー:' + column_name

    def check_length(self, columns, column_name, min, max):
        """
        文字数チェックを実施する。

        Parameters
        ----------
        columns : obj
            文字数チェックをする項目
        column_name: str
            項目名
        min : int
            最小桁数
        max : int
            最大桁数

        Returns
        -------
        str
            エラー内容
        """
        if type(columns) is int:
            columns = str(columns)

        if min and int(min) > len(columns):
            return f'文字数エラー（最小文字数[{min}]未満）:{column_name}'

        if max and int(max) < len(columns):
            return f'文字数エラー（最大文字数[{max}]超過）:{column_name}'

    def check_int(self, columns, column_name):
        """
        int型チェックを実施する。

        Parameters
        ----------
        columns : obj
            int型チェックをする項目
        column_name: str
            項目名

        Returns
        -------
        str
            エラー内容
        """
        if isinstance(columns, int):
            columns_replaced = True
        else:
            columns_replaced = columns.isnumeric()

        if columns is None or not columns_replaced:
            return 'int型チェックエラー:' + column_name

    def check_year_month(self, columns, column_name):
        """
        年月の形式をチェックする。

        Parameters
        ----------
        columns : obj
            形式チェックをする項目
        column_name: str
            項目名

        Returns
        -------
        str
            エラー内容
        """
        # 日付のハイフンとスラッシュ区切りに対応
        columns_replaced = columns.replace('-', '').replace('/', '')
        try:
            datetime.datetime.strptime(columns_replaced, "%Y%m")
        except ValueError:
            return f'年月形式エラー : {column_name}({columns})'

    def check_year_month_day(self, columns, column_name):
        """
        年月日の形式をチェックする。

        Parameters
        ----------
        columns : obj
            形式チェックをする項目
        column_name: str
            項目名

        Returns
        -------
        str
            エラー内容
        """
        # 日付のハイフンとスラッシュ区切りに対応
        columns_replaced = columns.replace('-', '').replace('/', '')
        try:
            datetime.datetime.strptime(columns_replaced, "%Y%m%d")
        except ValueError:
            return f'年月日形式エラー : {column_name}({columns})'

    def check_time_format(self, columns, column_name, time_format):
        """
        時間の形式をチェックする。

        Parameters
        ----------
        columns : obj
            形式チェックをする項目
        column_name: str
            項目名
        time_format: str
            チェックしたいフォーマット

        Returns
        -------
        str
            エラー内容
        """
        # 日付のハイフンとスラッシュ区切りに対応
        columns_replaced = columns.replace(':', '')
        try:
            datetime.datetime.strptime(columns_replaced, time_format)
        except ValueError:
            return f'時間形式エラー : {column_name}({columns})'
