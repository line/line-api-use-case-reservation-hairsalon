/**
 * ヘアサロンアプリケーションプラグイン
 *
 * @param {Object} $axios
 * @param {Object} app
 * @param {Object} store
 * @param {Object} env
 * @return {VueHairsalon} 
 */
const VueHairsalon = ($axios, app, store, env) => {
    /** @type {string} 通信モジュール */
    const _module = env.AJAX_MODULE ? env.AJAX_MODULE : "axios";
    /** @type {string} APIGatewayステージ名 */
    const _stage = `/${env.APIGATEWAY_STAGE}`;
    /** @type {Object} ロケール */
    let _i18n = app.i18n.messages[store.state.locale];

    return {
        /**
         * エリア＆店舗情報取得
         *
         * @return {Object} エリア＆店舗情報
         */
        async getAreaShops() {
            let ret = { areas: [], hairsalons: {} };
            // エリアレコード
            const arecord = ()=>{ return { code: null, name: null }; };
            // 店舗レコード
            const srecord = ()=>{
                return { 
                    id: null,
                    name: null,
                    img: null,
                    address: null,
                    start: null,
                    end: null,
                    holiday: null,
                    tel: null,
                    email: null,
                    line: null,
                    map: null,
                }; 
            };

            // エリア＆店舗データ取得
            let data = await this[_module].areaData();
            if (!data) { return ret };

            for (const record of data) {
                const areaId = record.areaId;
                const areaName = record.areaName;
                // エリア情報
                if (!(areaId in ret.hairsalons)) {
                    let area = arecord();
                    area.code = areaId;
                    area.name = areaName;
                    ret.areas.push(area);
                    ret.hairsalons[record.areaId] = [];
                }

                // 並び順変更
                record.shop.sort((previous, after)=>{
                    const val1 = previous.displayOrder;
                    const val2 = after.displayOrder;
                    if (val1 < val2) return -1;
                    if (val1 > val2) return 1;
                    return 0;
                });

                for (const shopRecord of record.shop) {
                    // 店舗情報
                    let shop = srecord();
                    shop.id = shopRecord.shopId;
                    shop.name = shopRecord.shopName;
                    shop.img = shopRecord.imageUrl;
                    shop.address = shopRecord.shopAddress;
                    shop.start = shopRecord.openTime;
                    shop.end = shopRecord.closeTime;
                    shop.holiday = app.$hairsalon.utils.convertWeekdays(shopRecord.closeDay);
                    shop.tel = shopRecord.shopTel;
                    shop.email = ("mailAddress" in shopRecord) ? shopRecord.mailAddress : null;
                    shop.line = shopRecord.lineAccountUrl;
                    shop.map = shopRecord.coordinate ? shopRecord.coordinate : null;

                    ret.hairsalons[record.areaId].push(shop);
                }
            }

            return ret;
        },

        /**
         * 店舗別スタッフ情報取得
         *
         * @param {number} shopId 店舗ID
         * @return {Array<Object>} 店舗別スタッフ情報
         */
        async getShopStaffs(shopId) {
            let ret = [];
            // スタッフレコード
            const srecord = ()=>{
                return { 
                    staffId: null,
                    name: null,
                    sex: null,
                    img: null,
                    career: null,
                    message: null,
                }; 
            };

            // エリア＆店舗データ取得
            const data = await this[_module].staffsData(shopId);
            if (!data) { return ret };

            // 並び順変更
            data.sort((previous, after)=>{
                const val1 = previous.displayOrder;
                const val2 = after.displayOrder;
                if (val1 < val2) return -1;
                if (val1 > val2) return 1;
                return 0;
            });

            for (const record of data) {
                let staff = srecord();
                staff.staffId = record.staffId;
                staff.name = record.staffName;
                staff.sex = record.gender==1 ? "male" : (record.gender==2 ? "female": "unknown");
                staff.img = record.imageUrl;
                staff.career = record.history;
                staff.message = record.message; 
                ret.push(staff);
            }

            return ret;
        },

        /**
         *　担当者月別 予約状況取得
         *
         * @param {number} shopId 店舗ID
         * @param {number} staffId スタッフID
         * @param {number} month 対象月
         * @param {Object} info 店舗、スタッフ情報
         * @return {Object} 担当者月別予約状況
         */
        async getStaffMonthlySchedule(shopId, staffId, month, info) {
            let ret = {};

            // 担当者月別予約状況データ取得
            const data = await this[_module].staffCalendarData(shopId, staffId, month, info.menu);
            if (!data) { return ret };

            // (担当者) 予約状況データ格納
            const yyyymm = data.calendarYearMonth.replace(/-/g, "");
            for (const dayRecord of data.calendarDays) {
                // 日別営業状態＆予約状況
                const dd = ("00"+dayRecord.day).slice(-2);
                const day = `${yyyymm.substr(0, 4)}-${yyyymm.substr(4, 2)}-${dd}`;
                const vacancyFlg = dayRecord.vacancyFlg==1 ? true : false;
                const workingStatus = app.$hairsalon.utils.isHoliday(day, info.shop.holiday);

                let schedule = app.$hairsalon.utils.createScheduleRecord();
                schedule.status = workingStatus ? 0 : (vacancyFlg ? 1 : 2);
                schedule.name = info.staff.name;
                schedule.start = info.shop.start;
                schedule.end = info.shop.end;

                ret[day] = schedule;
            }

            return ret;
        },

        /**
         *　担当者日別 予約状況取得　
         *
         * @param {number} shopId 店舗ID
         * @param {number} staffId スタッフID
         * @param {number} day 予約日
         * @param {Object} schedule 予約状況
         * @param {Object} hairsalon ヘアサロン店舗情報
         * @param {Object} menu メニュー情報
         * @param {Object} selectedMenu 指定メニュー情報
         * @return {Array<Object>} 担当者日別予約状況 
         */
        async getStaffDailySchedule(shopId, staffId, day, schedule, hairsalon, menu, selectedMenu) {
            let ret = [];

            // LIFF ID Token取得
            const idToken = store.state.lineUser.idToken;

            // 担当者月別予約状況データ取得
            const data = await this[_module].staffDailyData(idToken, shopId, staffId, day, schedule);
            if (!data) { return ret };

            if ("reservedInfo" in data) {
                for (const reservedRecord of data.reservedInfo) {
                    // 予約
                    let event = app.$hairsalon.utils.createEventRecord();
                    event.staffId = data.staffId; 
                    event.name = _i18n.hairsalon.reserved;
                    event.start = `${day} ${reservedRecord.reservedStartTime}`;
                    event.end = `${day} ${reservedRecord.reservedEndTime}`;
                    event.course = null;
                    event.color = "error";
                    ret.push(event);
                }
            }

            return app.$hairsalon.utils.insertEmptyEvents(ret, day, hairsalon, selectedMenu);
        },

        /**
         * コース情報取得
         *
         * @param {number} shopId 店舗ID
         * @return {Array<Object>} コース情報 
         */
        async getCourses(shopId) {
            let ret = [];

            // コースレコード
            const crecord = () => {
                return {
                    id: null,
                    name: null,
                    time: null,
                    price: null,
                    text: null,
                    value: null,                    
                }
            };

            // コースデータ取得
            const data = await this[_module].courseData(shopId);
            if (!data) { return ret };

            for (const record of data) {
                let course = crecord();
                course.id = record.courseId;
                course.name = record.courseName;
                course.time = parseInt(record.courseMinutes, 10);
                course.price = parseInt(record.price, 10);
                course.text = `${course.name} (${_i18n.hairsalon.yen.replace("{price}", course.price.toLocaleString())})`;
                course.value = course.id;
                ret.push(course);
            }

            return ret;
        },

        /**
         * 予約登録
         *
         * @param {string} token アクセストークン
         * @param {number} shopId 店舗ID
         * @param {number} day 予約日
         * @param {string} start 予約開始時間
         * @param {string} end 予約終了時間
         * @param {number} courseId コースID
         * @param {number} staffId スタッフID
         * @param {number} price 価格
         * @param {Object} names ユーザー、スタッフ、コース名称
         * @return {Object} 予約ID 
         */
        async updateReserve(token, shopId, day, start, end, courseId, staffId, price, names) {
            // LIFF ID Token取得
            const idToken = store.state.lineUser.idToken;
            // 送信パラメーター
            const params = {
                idToken: idToken,
                accessToken: token,
                shopId: shopId,
                shopName: names.shopName,
                reservationDate: day,
                reservationStarttime: start,
                reservationEndtime: end,
                courseId: courseId,
                courseName: names.courseName,
                userName: names.userName,
                staffId: staffId,
                staffName: names.staffName,
                amount: price,
            };
            // 予約登録
            const data = await this[_module].reserve(params);
            if (!data) { return null };

            // メッセージ
            let message = {
                reservationId: data.reservationId,
            };

            return message;
        },

        // ============================================
        //     ユーティリティ
        // ============================================
        utils: {
            /**
             *　年月リスト
             *
             * @param {number} count 月数
             * @return {Array<Object>} 年月リスト
             */
            monthList(count) {
                let months = [];
                let yyyymmdd = app.$utils.now("yyyymmdd");

                let yyyy = yyyymmdd.substr(0, 4);
                let mm = yyyymmdd.substr(4, 2).replace(/^0/, " ");
                if (_i18n.type == "en") { mm = app.$utils.englishMonth(mm); }
                months.push({ text: _i18n.hairsalon.yyyymm.replace("{year}", yyyy).replace("{month}", mm), value: `${yyyymmdd.substr(0, 6)}` });

                for (let i=0; i<count; i++) {
                    yyyymmdd = app.$utils.now("yyyymmdd", i+1);
                    yyyy = yyyymmdd.substr(0, 4);
                    mm = yyyymmdd.substr(4, 2).replace(/^0/, " ");
                    if (_i18n.type == "en") { mm = app.$utils.englishMonth(mm); }
                    months.push({ text: _i18n.hairsalon.yyyymm.replace("{year}", yyyy).replace("{month}", mm), value: `${yyyymmdd.substr(0, 6)}` });
                }
                
                return months;
            },

            /**
             *　時間帯リスト
             *
             * @param {string} fromTime 開始時間
             * @param {string} toTime 終了時間
             * @return {Array<Object>} 時間帯リスト 
             */
            timeList(fromTime, toTime) {
                let ret = [];
    
                let ftime = parseInt(fromTime.split(":")[0], 10);
                let ttime = parseInt(toTime.split(":")[0], 10);
    
                for (let tm=ftime; tm<=ttime; tm++) {
                    let time = ("00" + tm).slice(-2) + ":00";
                    let mtime = ("00" + tm).slice(-2) + ":30";
                    if (time >= fromTime) {
                        ret.push({ text: time, value: time });
                    }
                    if (mtime <= toTime) {
                        ret.push({ text: mtime, value: mtime });
                    }
                }
    
                return ret;
            },

            /**
             *　Storage読み込み
             *
             * @param {string} name ストレージ要素名
             * @return {any} 値 
             */
            readStore(name) {
                let hairsalon = app.$utils.ocopy(store.state.hairsalon);
                if (!hairsalon) { hairsalon = {}; }
                return (name in hairsalon) ? hairsalon[name] : null;
            },

            /**
             * Storage書き込み
             *
             * @param {string} name ストレージ要素名
             * @param {any} value 値
             */
            writeStore(name, value) {
                let hairsalon = app.$utils.ocopy(store.state.hairsalon);
                if (!hairsalon) { hairsalon = {}; }
                hairsalon[name] = value;
                store.commit("hairsalon", hairsalon);
            },

            /**
             * 時間帯重複判定
             *
             * @param {Array<Object>} events 予約イベント
             * @param {number} day 予約日
             * @param {string} start 予約開始時間
             * @param {string} end 予約終了時間
             * @return {boolean} 真偽値
             */
            isTimezoneOverlap(events, day, start, end) {
                let ret = false;

                const startDatetime = `${day} ${start}`;
                const endDatetime = `${day} ${end}`;
                for (const event of events) {
                    const color = event.color;
                    if (color == "info" || color == "warning") { continue; }
                    
                    const fromDatetime = event.start;
                    const toDatetime = event.end;
                    // 時間帯重複チェック
                    if (fromDatetime >= startDatetime && fromDatetime < endDatetime) {
                        ret = true;
                    } else if (toDatetime > startDatetime && toDatetime <= endDatetime) {
                        ret = true;
                    } else if (fromDatetime <= startDatetime && toDatetime >= endDatetime) {
                        ret = true;
                    }
                    if (ret) break;
                }
    
                return ret;
            },

            /**
             * 曜日値変換（ヘアサロン仕様 --> Javascript仕様）
             *
             * @param {Array<number>} weekdays
             * @return {Array<number>} 変換済曜日配列 
             */
            convertWeekdays(weekdays) {
                let ret = [];

                for (let weekday of weekdays) {
                    switch (weekday) {
                    case 0: ret.push(-1); break;  // 休日なし
                    case 1: ret.push(1); break;  // 月
                    case 2: ret.push(2); break;  // 火
                    case 3: ret.push(3); break;  // 水
                    case 4: ret.push(4); break;  // 木
                    case 5: ret.push(5); break;  // 金
                    case 6: ret.push(6); break;  // 土
                    case 7: ret.push(0); break;  // 日
                    case 9: ret.push(9); break;  // 祝
                    }
                }

                return ret;
            },

            /**
             *　休日判定
             *
             * @param {string} yyyymmdd 日付
             * @param {Array<number>} holiday 休日曜日情報
             * @return {boolean} 真偽値
             */
            isHoliday(yyyymmdd, holiday) {
                let ret = false;
                let date = new Date(yyyymmdd.replace(/-/g, "/"))
                let weekday = date.getDay();
                if (holiday != null && holiday.length > 0 && holiday.indexOf(weekday) >= 0) {
                    ret = true;
                }
                return ret;
            },

            /**
             *　スケジュールレコード生成
             *
             * @return {Object} スケジュールレコード 
             */
            createScheduleRecord() {
                return { 
                    status: 1,
                    name: null,
                    start: null,
                    end: null,
                    events: [],
                }; 
            },

            /**
             * イベントレコード生成
             *
             * @return {Object} イベントレコード 
             */
            createEventRecord() {
                return {
                    staffId: null,
                    name: null,
                    start: null,
                    end: null,                    
                    course: null,
                    color: null,
                };
            },

            /**
             * 予約空き時間イベント挿入
             *
             * @param {Array<Object>} events 予約イベント
             * @param {number} day 予約日
             * @param {Object} hairsalon ヘアサロン店舗情報
             * @param {Object} selectedMenu 指定メニュー情報
             * @return {Object} 空き時間イベント挿入済予約イベント 
             */
            insertEmptyEvents(events, day, hairsalon, selectedMenu) {            
                let emptyEvents = [];

                // ヘアサロン開始・終了時間
                const start = `${day.replace(/-/g, "/")} ${hairsalon.start}`;
                const end = `${day.replace(/-/g, "/")} ${hairsalon.end}`;
                let fdate = new Date(start);
                let tdate = new Date(end);
                // 営業時間帯
                let ftime = fdate.getTime();
                let ttime = tdate.getTime();
                // 施術時間
                let minutes = parseInt(selectedMenu.time, 10);

                // 並び変え
                events.sort((previous, after)=>{
                    const val1 = previous.start;
                    const val2 = after.start;
                    if (val1 < val2) return -1;
                    if (val1 > val2) return 1;
                    return 0;
                });

                let startTimePointer = start.replace(/\//g, "-");
                let endTimePointer = end.replace(/\//g, "-");
                for (let event of events) {
                    // イベント開始・終了時間
                    let eventStart = event.start;
                    let eventEnd = event.end;

                    // 時間帯ループ
                    for (let dt=ftime; dt<=ttime; dt=(dt+(1000 * 60 * 30))) {
                        const startDate = new Date(dt);
                        const endDate = new Date(dt+(1000 * 60 * minutes));
                        const stime = `${day} ${("00"+startDate.getHours()).slice(-2)}:${("00"+startDate.getMinutes()).slice(-2)}`;
                        const etime = `${day} ${("00"+endDate.getHours()).slice(-2)}:${("00"+endDate.getMinutes()).slice(-2)}`;

                        if (stime == eventStart) {
                            // 前方空き時間埋め
                            if (startTimePointer  < stime) {
                                emptyEvents.push((()=>{
                                    return {
                                        staffId: event.staffId,
                                        name: _i18n.hairsalon.not_reserve,
                                        start: startTimePointer,
                                        end: eventStart,
                                        course: selectedMenu.id,
                                        color: "warning",
                                    };
                                })());
                            }
                            emptyEvents.push(event);
                            startTimePointer = eventEnd;
                            dt = (new Date(eventEnd.replace(/-/g, ""))).getTime();
                        }
                    }
                }
                // 後方空き時間埋め
                if (startTimePointer < endTimePointer) {
                    emptyEvents.push((()=>{
                        return {
                            staffId: null,
                            name: _i18n.hairsalon.not_reserve,
                            start: startTimePointer,
                            end: endTimePointer,
                            course: selectedMenu.id,
                            color: "warning",
                        };
                    })());
                }

                // 施術時間以上イベント修正・間引き
                for (let [index, event] of emptyEvents.entries()) {
                    if (event.color == "warning") {
                        let eventStart = (new Date(event.start.replace(/-/g, "/"))).getTime();
                        let eventEnd = (new Date(event.end.replace(/-/g, "/"))).getTime();
                        let eventMinutes = (eventEnd - eventStart) / 60 / 1000;
                        if (eventMinutes >= minutes) {
                            let eventTime = eventEnd - ((minutes - 30) * 60 * 1000);
                            event.start = app.$utils.dateFormat(new Date(eventTime), "yyyy-mm-dd hh:mi");
                            if (event.start == event.end) {
                                    emptyEvents.splice(index, 1);
                            }
                        }
                    }
                }

                // 並び変え
                emptyEvents.sort((previous, after)=>{
                    const val1 = previous.start;
                    const val2 = after.start;
                    if (val1 < val2) return -1;
                    if (val1 > val2) return 1;
                    return 0;
                });

                return emptyEvents;
            }
        },

        // ============================================
        //     Lambdaアクセス (Axios)
        // ============================================
        axios: {
            /**
             * 店舗一覧取得API
             *
             * @return {Object} APIレスポンス内容
             */
            areaData: async() => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                }
                const response = await $axios.get(`${_stage}/shop_list_get`, { params: params });
                return response.status==200 ? response.data : null;
            },

            /**
             * 担当者一覧取得API
             *
             * @param {number} shopId 店舗ID
             * @return {Object} APIレスポンス内容
             */
            staffsData: async(shopId) => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                    shopId: shopId,
                }
                // GET送信
                const response = await $axios.get(`${_stage}/staff_list_get`, { params: params });
                return response.status==200 ? response.data : null;
            },

            /**
             * コース詳細情報取得API
             *
             * @param {number} shopId 店舗ID
             * @return {Object} APIレスポンス内容
             */
            courseData: async(shopId) => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                    shopId: shopId,
                }
                // GET送信
                const response = await $axios.get(`${_stage}/course_list_get`, { params: params });
                return response.status==200 ? response.data : null;
            },

            /**
             * 担当者カレンダー取得API
             *
             * @param {number} shopId 店舗ID
             * @param {number} staffId スタッフID
             * @param {string} month 年月
             * @param {Object} menu メニュー情報
             * @return {Object} APIレスポンス内容
             */
            staffCalendarData: async(shopId, staffId, month, menu) => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                    shopId: shopId,
                    staffId: staffId,
                    courseMinutes: menu.time,
                    preferredYearMonth: `${month.substr(0, 4)}-${month.substr(4, 2)}`,
                };
                // GET送信
                const response = await $axios.get(`${_stage}/staff_calendar_get`, { params: params });
                return response.status==200 ? response.data : null;
            },

            /**
             * 予約済時間取得API
             *
             * @param {string} idToken IDトークン
             * @param {number} shopId 店舗ID
             * @param {number} staffId スタッフID
             * @param {string} day 予約日時
             * @return {Object} APIレスポンス内容 
             */
            staffDailyData: async(idToken, shopId, staffId, day) => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                    shopId: shopId,
                    staffId: staffId,
                    idToken: idToken,
                    preferredDay: day,
                };
                // GET送信
                const response = await $axios.get(`${_stage}/reserved_time_get`, { params: params });
                return response.status==200 ? response.data : null;
            },

            /**
             * 予約登録API
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            reserve: async(params) => {
                // 送信パラメーター
                params['locale'] = store.state.locale;
                // POST送信
                const response = await $axios.post(`${_stage}/reservation_put`, params);
                return response.status==200 ? response.data : null;
            },
        },

        // ============================================
        //     Lambdaアクセス (Amplify API)
        // ============================================
        amplify: {
            /**
             * 店舗一覧取得API
             *
             * @return {Object} APIレスポンス内容
             */
            areaData: async() => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/shop_list_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },

            /**
             * 担当者一覧取得API
             *
             * @param {number} shopId 店舗ID
             * @return {Object} APIレスポンス内容
             */
            staffsData: async(shopId) => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                        shopId: shopId,
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/staff_list_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },

            /**
             * コース詳細情報取得API
             *
             * @param {number} shopId 店舗ID
             * @return {Object} APIレスポンス内容
             */
            courseData: async(shopId) => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                        shopId: shopId,
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/course_list_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },

            /**
             * 担当者カレンダー取得API
             *
             * @param {number} shopId 店舗ID
             * @param {number} staffId スタッフID
             * @param {string} month 年月
             * @param {Object} menu メニュー情報
             * @return {Object} APIレスポンス内容
             */
            staffCalendarData: async(shopId, staffId, month, menu) => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                        shopId: shopId,
                        staffId: staffId,
                        courseMinutes: menu.time,
                        preferredYearMonth: `${month.substr(0, 4)}-${month.substr(4, 2)}`,
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/staff_calendar_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
            // 予約済時間取得API
            staffDailyData: async(idToken, shopId, staffId, day) => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                        shopId: shopId,
                        staffId: staffId,
                        idToken: idToken,
                        preferredDay: day,
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/reserved_time_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },

            /**
             * 予約登録API
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            reserve: async(params) => {
                let response = null;
                // 送信パラメーター
                params['locale'] = store.state.locale;
                const myInit = {
                    body: params,
                };
                // POST送信
                try {
                    response = await app.$amplify.API.post("LambdaAPIGateway", `${_stage}/reservation_put`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
        },

    }
}

export default ({ $axios, app, store, env }, inject) => {
    inject("hairsalon", VueHairsalon($axios, app, store, env));
}
