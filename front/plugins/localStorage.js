import CreatePersistedState from "vuex-persistedstate"

/**
 *　ローカルストレージプラグイン
 *
 * @param {Object} env
 * @param {Object} store
 */
export default ({ env, store }) => {
    CreatePersistedState({
      key: "liff-usecase",
      paths: [
        'started',
        'locale',
      ],
      storage: window.localStorage
    })(store);
}
