from common import const


def create_flex_message(**kwargs):
    """
    予約完了通知用flexメッセージを作成

    Parameters
    ----------
    reservation_shop : str
        予約店舗
    reservation_date : str
        予約日
    course_name : str
        予約コース名
    staff_name : str
        担当スタッフ名
    remind_status : str
        リマインドステータス
    Returns
    -------
    result : dict
        Flexmessageの元になる辞書型データ
    """
    shop_name = kwargs['shop_name']
    shop_address = kwargs['shop_address']
    reservation_date = kwargs['reservation_date']
    course_name = kwargs['course_name']
    staff_name = kwargs['staff_name']
    remind_status = kwargs['remind_status']

    # メッセージを確定
    if remind_status == 'day_before':
        notification_type = "リマインド通知"
        remind_header_msg = "ご予約日の" + kwargs['day_before'] + "日前となりました"
        remind_last_msg = "当日は、お会いできることを心よりお待ちしています。"
    elif remind_status == 'on_day':
        notification_type = "リマインド通知"
        remind_header_msg = "ご予約日の当日となりました"
        remind_last_msg = "本日は、お会いできることを心よりお待ちしています。\nどうぞお気をつけてお越しください。"
    else:
        notification_type = "ご予約確定通知"
        remind_header_msg = "ご予約を承りました"
        remind_last_msg = "当日は、お会いできることを心よりお待ちしています。\nご予約をキャンセルされる場合は、お電話にてご連絡ください。"  # noqa 501

    flex_msg = {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "flex": 0,
                "contents": [
                    {
                        "type": "text",
                        "text": notification_type,
                        "size": "sm",
                        "weight": "bold",
                        "color": "#36DB34"
                    },
                    {
                        "type": "text",
                        "text": remind_header_msg,
                        "size": "lg",
                        "weight": "bold"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "margin": "xs",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "店舗名:",
                                        "flex": 1,
                                        "size": "sm",
                                        "align": "start",
                                        "color": "#5B5B5B"
                                    },
                                    {
                                        "type": "text",
                                        "text": shop_name,
                                        "flex": 2,
                                        "size": "sm",
                                        "align": "start",
                                        "color": "#666666",
                                        "wrap": True
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "店舗住所:",
                                        "flex": 1,
                                        "size": "sm",
                                        "align": "start",
                                        "color": "#5B5B5B"
                                    },
                                    {
                                        "type": "text",
                                        "text": shop_address,
                                        "flex": 2,
                                        "size": "sm",
                                        "align": "start",
                                        "color": "#666666",
                                        "wrap": True
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "日時:",
                                        "flex": 1,
                                        "size": "sm",
                                        "color": "#5B5B5B"
                                    },
                                    {
                                        "type": "text",
                                        "text": reservation_date,
                                        "flex": 2,
                                        "size": "sm",
                                        "align": "start",
                                        "color": "#666666",
                                        "wrap": True
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "コース:",
                                        "flex": 1,
                                        "size": "sm",
                                        "color": "#5B5B5B"
                                    },
                                    {
                                        "type": "text",
                                        "text": course_name,
                                        "flex": 2,
                                        "size": "sm",
                                        "align": "start",
                                        "color": "#666666",
                                        "wrap": True
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "担当スタッフ:",
                                        "flex": 1,
                                        "size": "sm",
                                        "color": "#5B5B5B"
                                    },
                                    {
                                        "type": "text",
                                        "text": staff_name,
                                        "flex": 2,
                                        "size": "sm",
                                        "align": "start",
                                        "color": "#666666",
                                        "wrap": True
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": remind_last_msg,
                                        "size": "sm",
                                        "color": "#4A4141",
                                        "wrap": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }

    return flex_msg