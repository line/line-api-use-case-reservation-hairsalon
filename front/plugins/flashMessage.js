import Vue from "vue"

/**
 * フラッシュメッセージプラグイン
 *
 * @return {Object} 
 */
const VueFlashMessage = () => {

    let _message = {};

    return {
        get(name) {
            if (name in _message) {
                const ret = Vue.util.extend(_message[name]);
                delete _message[name];
                return ret;
            }
            return undefined;
        },
        set(name, value) {
            _message[name] = value;
        },
        hold(name) {
            return _message[name];
        },
        clear(name) {
            if (name === undefined) {
                _message = {};
            } else if (name in _message) {
                delete _message[name];
            }
        }
    };
}

export default ({}, inject) => {
    inject("flash", VueFlashMessage());
}
