/**
 * Vuetify Awesomeフォントプラグイン
 *
 */
import "vuetify/dist/vuetify.min.css"
import '@mdi/font/css/materialdesignicons.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@fortawesome/fontawesome-free/css/all.css'
import 'font-awesome/css/font-awesome.min.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'

import Vue from "vue"
import Vuetify from "vuetify/lib"

Vue.use(Vuetify)
library.add(fas) 

export default new Vuetify({
    icons: {
        iconfont: "mdi" || "mdiSvg" || "md" || "fa" || "fa4" || "faSvg"
    },
})
