import Vue from "vue"
import VueI18n from "vue-i18n"

Vue.use(VueI18n)

/**
 *　多言語化プラグイン
 *
 * @param {Object} app
 * @param {Object} store
 */
export default ({ app, store }) => {
    app.i18n = new VueI18n({
        locale: store.state.locale,
        fallbackLocale: "ja",
        messages: {
            ja: require("~/locales/ja.json")
        }
    })
}
