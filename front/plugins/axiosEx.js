/**
 * Axios拡張プラグイン
 *
 * @param {Object} $axios
 * @param {Object} store
 */
export default({ $axios, app, store }) => {
    // リクエスト拡張
    $axios.onRequest((config)=>{

    });
    // レスポンス拡張
    $axios.onResponse((response)=>{
        
    });
    // エラー拡張
    $axios.onError((error)=>{
        return app.$utils.showHttpError(error);
    });
}
    