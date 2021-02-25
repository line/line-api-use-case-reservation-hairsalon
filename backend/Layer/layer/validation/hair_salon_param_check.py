from validation.param_check import ParamCheck


class HairSalonParamCheck(ParamCheck):
    def __init__(self, params):
        self.shop_id = params['shopId'] if 'shopId' in params else None
        self.shop_name = params['shopName'] if 'shopName' in params else None
        self.staff_id = params['staffId'] if 'staffId' in params else None
        self.staff_name = params['staffName'] if 'staffName' in params else None  # noqa:E501
        self.user_name = params['userName'] if 'userName' in params else None
        self.course_minutes = params['courseMinutes'] if 'courseMinutes' in params else None  # noqa:E501
        self.preferred_year_month = params['preferredYearMonth'] if 'preferredYearMonth' in params else None  # noqa:E501
        self.preferred_day = params['preferredDay'] if 'preferredDay' in params else None  # noqa:E501
        self.reservation_date = params['reservationDate'] if 'reservationDate' in params else None  # noqa:E501
        self.reservation_starttime = params['reservationStarttime'] if 'reservationStarttime' in params else None  # noqa:E501
        self.reservation_endtime = params['reservationEndtime'] if 'reservationEndtime' in params else None  # noqa:E501
        self.access_token = params['accessToken'] if 'accessToken' in params else None  # noqa: E501
        self.course_id = params['courseId'] if 'courseId' in params else None
        self.course_name = params['courseName'] if 'courseName' in params else None  # noqa: E501
        self.amount = params['amount'] if 'amount' in params else None

        self.error_msg = []

    def check_api_staff_list_get(self):
        self.check_shop_id()

        return self.error_msg

    def check_api_course_list_get(self):
        self.check_shop_id()

        return self.error_msg

    def check_api_staff_calendar_get(self):
        self.check_staff_id()
        self.check_course_minutes()
        self.check_preferred_year_month()

        return self.error_msg

    def check_api_reserved_time_get(self):
        self.check_staff_id()
        self.check_preferred_day()

        return self.error_msg

    def check_api_reservation_put(self):
        self.check_user_name()
        self.check_access_token()
        self.check_shop_id()
        self.check_shop_name()
        self.check_reservation_date()
        self.check_reservation_starttime()
        self.check_reservation_endtime()
        self.check_course_id()
        self.check_course_name()
        self.check_staff_id()
        self.check_staff_name()
        self.check_amount()

        return self.error_msg

    def check_shop_id(self):
        if error := self.check_required(self.shop_id, 'shopId'):
            self.error_msg.append(error)
            return

        if error := self.check_int(self.shop_id, 'shopId'):
            self.error_msg.append(error)
            return

    def check_shop_name(self):
        if error := self.check_required(self.shop_name, 'shopName'):
            self.error_msg.append(error)
            return

    def check_staff_id(self):
        if error := self.check_required(self.staff_id, 'staffId'):
            self.error_msg.append(error)
            return

        if error := self.check_int(self.shop_id, 'staffId'):
            self.error_msg.append(error)
            return

    def check_staff_name(self):
        if error := self.check_required(self.staff_name, 'staffName'):
            self.error_msg.append(error)
            return

    def check_course_minutes(self):
        if error := self.check_required(self.course_minutes,
                                        'courseMinutes'):
            self.error_msg.append(error)
            return

        if error := self.check_int(self.course_minutes,
                                   'courseMinutes'):
            self.error_msg.append(error)

    def check_preferred_year_month(self):
        if error := self.check_required(self.preferred_year_month,
                                        'preferredYearMonth'):
            self.error_msg.append(error)
            return

        if error := self.check_year_month(self.preferred_year_month,
                                          'preferredYearMonth'):
            self.error_msg.append(error)

    def check_user_name(self):
        if error := self.check_required(self.user_name, 'userName'):
            self.error_msg.append(error)
            return

        if error := self.check_length(self.user_name, 'userName', 1, None):
            self.error_msg.append(error)

    def check_preferred_day(self):
        if error := self.check_required(self.preferred_day, 'preferredDay'):
            self.error_msg.append(error)
            return

        if error := self.check_year_month_day(self.preferred_day, 'preferredDay'):  # noqa 501
            self.error_msg.append(error)

    def check_access_token(self):
        if error := self.check_required(self.access_token, 'accessToken'):
            self.error_msg.append(error)
            return

        if error := self.check_length(self.access_token,
                                      'accessToken', 1, None):
            self.error_msg.append(error)

    def check_course_id(self):
        if error := self.check_required(self.course_id, 'courseId'):
            self.error_msg.append(error)
            return

        if error := self.check_int(self.amount, 'amount'):
            self.error_msg.append(error)

    def check_course_name(self):
        if error := self.check_required(self.course_name, 'courseName'):
            self.error_msg.append(error)
            return

    def check_reservation_date(self):
        if error := self.check_required(self.reservation_date, 'checkReservationDate'):  # noqa 501
            self.error_msg.append(error)
            return

        if error := self.check_year_month_day(self.reservation_date, 'checkReservationDate'):  # noqa 501
            self.error_msg.append(error)

    def check_reservation_starttime(self):
        if error := self.check_required(self.reservation_starttime, 'checkReservationStarttime'):  # noqa 501
            self.error_msg.append(error)
            return

        if error := self.check_time_format(self.reservation_starttime, 'checkReservationStarttime', '%H%M'):  # noqa 501
            self.error_msg.append(error)
            return

    def check_reservation_endtime(self):
        if error := self.check_required(self.reservation_endtime, 'checkReservationEndtime'):  # noqa 501
            self.error_msg.append(error)
            return

        if error := self.check_time_format(self.reservation_endtime, 'checkReservationEndtime', '%H%M'):  # noqa 501
            self.error_msg.append(error)
            return

    def check_amount(self):
        if error := self.check_required(self.amount, 'amount'):
            self.error_msg.append(error)
            return

        if error := self.check_int(self.amount, 'amount'):
            self.error_msg.append(error)
