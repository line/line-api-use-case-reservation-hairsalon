import json
import logging
import os

from common import common_const, utils
from hair_salon.hair_salon_user_setting import UserSetting
from validation import hair_salon_param_check as validation

# 環境変数
HAIR_SALON_M_SHOP_DB = os.environ.get("HAIR_SALON_M_SHOP_DB")
# ログ出力の設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# テーブル操作クラスの初期化
user_setting_table_controller = UserSetting()


def lambda_handler(event, context):
    """
    ユーザー設定情報を返却する
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    user_setting : dict
        スタッフ一覧情報
    """
    # パラメータログ、チェック
    logger.info(event)
    params = event['queryStringParameters']

    if params is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)

    # param_checker = validation.HairSalonParamCheck(
    #     params)
    # if error_msg := param_checker.check_api_staff_list_get():
    #     error_msg_display = ('\n').join(error_msg)
    #     logger.error(error_msg_display)
    #     return utils.create_error_response(error_msg_display, 400)

    try:
        # 店舗IDでスタッフ情報を取得
        user_setting = user_setting_table_controller.update_item(
            user_id = str(params['userId']),
            profile_image_url = str(params['profileImageUrl']),
            )
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')
        
    print(user_setting)
    body = json.dumps(
        user_setting,
        default=utils.decimal_to_int, ensure_ascii=False)
    return utils.create_success_response(body)
