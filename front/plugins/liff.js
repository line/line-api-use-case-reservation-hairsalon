/**
 *　LIFFプラグイン
 *
 * @param {Object} context
 * @return {Object} 
 */
const VueLiff = (context) => {

    return {
        /**
         * LIFF初期化
         *
         * @param {Function} callback コールバック関数
         * @return {any} 戻り値
         */
        async init(callback) {
            await liff.init({ liffId: context.env.LIFF_ID });
            if (!liff.isLoggedIn()) { 
                context.redirect("/");
            } else {
                return callback();
            }
        },
        /**
         * LIFFプロファイル取得
         *
         * @return {Object} LIFFプロファイル情報 
         */
        async getLiffProfile() {
            // LIFF Profile
            const profilePromise = liff.getProfile();
            const tokenPromise = liff.getAccessToken();
            const idTokenPromise = liff.getIDToken();
            const profile = await profilePromise;
            const token = await tokenPromise;
            const idToken = await idTokenPromise;

            const lineUser = {
                expire: (new Date()).getTime() + (1000 * 60 * 30),
                userId: profile.userId,
                name: profile.displayName,
                image: profile.pictureUrl,
                token: token,
                idToken: idToken,
            };

            return lineUser;
        },
   
    }
}

export default (context, inject) => {
    inject("liff", VueLiff(context));
}
