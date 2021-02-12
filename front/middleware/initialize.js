/**
 * 初期処理ミドルウェア
 *
 * @param {Object} context
 */
export default async (context) => {
    /** @type {boolean} 初期化済フラグ */
    const inited = context.app.$flash.hold("LIFF_INITED");

    /**
     *　LIFFプロファイル取得・設定
     *
     */
    const _settingLiffProfile = async() => {
        const lineUser = await context.app.$liff.getLiffProfile();
        context.store.commit("lineUser", lineUser);
    }

    // LIFF Login & Profile
    if (inited) { 
        const lineUser = context.store.state.lineUser;
        if (!lineUser || !("expire" in lineUser)) {
            // Get LIFF Profile & Token
            _settingLiffProfile();
        } else {
            const now = new Date();
            const expire = parseInt(lineUser.expire, 10);
            if (expire < now.getTime()) {
                // Get LIFF Profile & Token
                _settingLiffProfile();
            }
        }
    } else {
        // 起動時間
        context.store.commit("started", new Date().toLocaleString({ timeZone: "Asia/Tokyo" }));
        // 言語
        if ("lang" in context.query) {
            context.store.commit("locale", context.query.lang);
            context.app.i18n.locale = context.store.state.locale;
        } else if (context.store.state.locale) {
            context.app.i18n.locale = context.store.state.locale;
        } 

        // LIFF Initialize
        liff.init({ liffId: context.env.LIFF_ID })
        .then(() => {
            context.app.$flash.set("LIFF_INITED", true);
            const loggedIn = liff.isLoggedIn();
            if (!loggedIn) {
                liff.login();
            }
        })
        .catch((err) => {
            console.log(err);
        });
    }

}
