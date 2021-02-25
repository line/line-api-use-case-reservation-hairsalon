/**
 * ユーティリティープラグイン
 *
 * @param {Object} app
 * @param {Object} store
 * @return {Object} 
 */
const VueUtils = (app, store) => {
    /** @type {Object} ロケール */
    let _i18n = app.i18n.messages[store.state.locale];

    // ==============================================
    //  Public Methods
    // ==============================================
    const _functions = {
        /**
         * オブジェクトコピー
         *
         * @param {Object} obj コピー元オブジェクト
         * @return {Object} コピーオブジェクト
         */
        ocopy(obj) {
            let ret = null;
            if (obj != null) {
                ret = JSON.parse(JSON.stringify(obj));
            }
            return ret;
        },

        /**
         * 日付フォーマット
         *
         * @param {Object} date 日付オブジェクト
         * @param {string} format 指定日付フォーマット
         * @return {string} 日付文字列
         */
        dateFormat(date, format) {
            return _dateformat(date, format);
        },

        /**
         * 現在日付取得
         *
         * @param {string} format 指定日付フォーマット
         * @param {number} addMonths 月数加算
         * @return {string} 日付文字列
         */
        now(format, addMonths) {
            let date = new Date();
            if (typeof(addMonths) == "number") {
                // 月末日処理
                const endDayOfMonth = new Date(date.getFullYear(), date.getMonth()+addMonths+1, 0);
                date.setMonth(date.getMonth() + addMonths);
                if (date.getTime() > endDayOfMonth.getTime()) {
                    date = endDayOfMonth;
                }
            }
            return _dateformat(date, format);
        },

        /**
         *　乱数生成
         *
         * @param {number} min 最小値
         * @param {number} max 最大値
         * @return {number} 乱数 
         */
        random(min, max) {
            return Math.floor((max - min + 1) * Math.random()) + min;
        },

        /**
         *　曜日変換（値-->名）
         *
         * @param {number|string} weekday 曜日値
         * @return {string} 曜日名 
         */
        weekdayName(weekday) {
            let name = "";

            switch (parseInt(weekday, 10)) {
            case 0: name = _i18n.utils.sun; break;
            case 1: name = _i18n.utils.mon; break;
            case 2: name = _i18n.utils.tue; break;
            case 3: name = _i18n.utils.wed; break;
            case 4: name = _i18n.utils.thu; break;
            case 5: name = _i18n.utils.fri; break;
            case 6: name = _i18n.utils.sat; break;
            }

            return name;
        },

        /**
         *　月名英語変換（値-->英語名）
         *
         * @param {number|string} month 月値
         * @return {string} 月英語名 
         */
        englishMonth(month) {
            let engMonth = null;

            switch (parseInt(month, 10)) {
            case 1: engMonth = "Jan."; break;   // January
            case 2: engMonth = "Feb."; break;   // February
            case 3: engMonth = "Mar."; break;   // March
            case 4: engMonth = "Apr."; break;   // April
            case 5: engMonth = "May."; break;   // May
            case 6: engMonth = "Jun."; break;   // June
            case 7: engMonth = "Jul."; break;   // July
            case 8: engMonth = "Aug."; break;   // August
            case 9: engMonth = "Sep."; break;   // September
            case 10: engMonth = "Oct."; break;  // October
            case 11: engMonth = "Nov."; break;  // November
            case 12: engMonth = "Dec."; break;  // December
            }

            return engMonth;
        },

        /**
         * 日付分加算
         *
         * @param {string} datetime 日付
         * @param {number} minutes 加算分数
         * @return {Object} 日付オブジェクト
         */
        addMinutes(datetime, minutes) {
            const date = new Date(datetime.replace(/-/g, "/"));
            date.setMinutes(date.getMinutes() + minutes);

            return date;
        },

        /**
         *　iOS判定
         *
         * @return {boolean} 真偽値
         */
        isIOS() {
            const userAgent = navigator.userAgent.toLowerCase();
            return (userAgent.indexOf("iphone")>=0 || userAgent.indexOf("ipad")>=0 || userAgent.indexOf("ipod")>=0); 
        },

        /**
         *　Android判定
         *
         * @return {boolean} 真偽値
         */
        isAndroid() {
            const userAgent = navigator.userAgent.toLowerCase();
            return (userAgent.indexOf("android")>=0);
        },

        /**
         * 地図アプリ起動
         *
         * @param {number} latitude 緯度
         * @param {number} longitude 経度
         * @param {number} zoom ズーム
         * @param {boolean} [markered=true] マーカー有無
         */
        openMapApp(latitude, longitude, zoom, markered=true) {
            let params = `ll=${latitude},${longitude}&z=${zoom}`;
            if (markered) {
                params += `&q=${latitude},${longitude}`;
            }

            if (app.$utils.isIOS()) {
                liff.openWindow({ url: `https://maps.apple.com/maps?${params}`, external: true });
            } else if (app.$utils.isAndroid()) {
                liff.openWindow({ url: `https://maps.google.com/maps?${params}`, external: true });
            } else {
                window.open(`https://maps.google.com/maps?${params}`, "_blank");
            }
        },

        /**
         * LINE公式アカウント開始
         *
         * @param {*} line
         */
        openLineOA(line) {
            if (app.$utils.isIOS()) {
                location.href = line;
            } else if (app.$utils.isAndroid()) {
                location.href = line;
            } else {
                window.open(line, "_blank");
            }
        },

        /**
         * HTTPエラー表示
         *
         * @param {Object} error
         */
        showHttpError(error) {
            if (error.response && error.response.status >= 400) {
                // HTTP 403 Topへ画面遷移
                if (error.response.status == 403) {
                    const errmsg = error.response.data ? error.response.data : _i18n.error.msg005;
                    window.alert(errmsg);
                    window.location = `https://liff.line.me/${process.env.LIFF_ID}`;
                    return true;
                }
    
                const response = error.response;
                setTimeout(() => {
                    store.commit("axiosError", `status=${response.status} ${response.statusText} ${response.data}`);
                }, 500);
                return true;
            }
            return false;
        },
    };

    // ==============================================
    //  Private Methods
    // ==============================================

    /**
     * 日付フォーマット
     *
     * @param {Object} date 日付オブジェクト
     * @param {string} format 指定日付フォーマット
     * @return {string} 日付文字列
     */
    const _dateformat = (date, format) => {
        const yyyy = date.getFullYear();
        const mm = ("00" + (date.getMonth() + 1)).slice(-2);
        const dd = ("00" + date.getDate()).slice(-2);
        const hh = ("00" + date.getHours()).slice(-2);
        const mi = ("00" + date.getMinutes()).slice(-2);
        const ss = ("00" + date.getSeconds()).slice(-2);

        let ret = `${yyyy}/${mm}/${dd} ${hh}:${mi}:${ss}`;
        if (format !== undefined) {
            let strFormat = format.toLowerCase();
            strFormat = strFormat.replace("yyyy", yyyy);
            strFormat = strFormat.replace("mm", mm);
            strFormat = strFormat.replace("dd", dd);
            strFormat = strFormat.replace("hh", hh);
            strFormat = strFormat.replace("mi", mi);
            strFormat = strFormat.replace("ss", ss);
            ret = strFormat;
        }

        return ret;
    };

    return _functions;

}

export default ({ app, store }, inject) => {
    inject("utils", VueUtils(app, store));
}
