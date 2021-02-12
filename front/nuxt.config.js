import fs from 'fs'
import dotenv from 'dotenv'

dotenv.config();

export default {
    telemetry: false,
    mode: 'spa',
    generate: {
        dir: './dist'
    },
    server: {
        port: 3000,
        host: '0.0.0.0',
        timing: false,
        https: {
            key: fs.readFileSync('./cert/localhost.key'),
            cert: fs.readFileSync('./cert/localhost.crt')
        }
    },
    target: 'server',
    router: {
        extendRoutes(routes, resolve) {
            routes.push({
                name: "notfound",
                path: "*",
                component: resolve(__dirname, "pages/error/404.vue")
            });
        }
    },
    head: {
        title: 'Use Case Application',
        meta: [
            { charset: 'utf-8' },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
        ],
        link: [
            { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        ],
        script: [
            { src: 'https://static.line-scdn.net/liff/edge/versions/2.5.0/sdk.js' },
        ],
    },
    loading: {
        color: '#00ba00',
    },
    css: [

    ],
    plugins: [
        { src: '~/plugins/i18n.js', mode: 'client' },
        { src: '~/plugins/localStorage.js', mode: 'client' },
        { src: '~/plugins/sessionStorage.js', mode: 'client' },
        { src: '~/plugins/axiosEx.js', mode: 'client' },
        { src: '~/plugins/amplify.js', mode: 'client' },
        { src: '~/plugins/vuetify.js', mode: 'client' },
        { src: '~/plugins/noreload.js', mode: 'client' },
        { src: '~/plugins/flashMessage.js', mode: 'client' },
        { src: '~/plugins/processing.js', mode: 'client' },
        { src: '~/plugins/utils.js', mode: 'client' },
        { src: '~/plugins/liff.js', mode: 'client' },
        { src: '~/plugins/app/hairsalon.js', mode: 'client' },
    ],
    components: true,
    buildModules: [
        '@nuxtjs/vuetify',
    ],
    modules: [
        '@nuxtjs/axios',
        '@nuxtjs/dotenv',
    ],
    build: {
    },
    axios: {
        baseURL: process.env.BASE_URL,
    },
    env: {
        LIFF_ID: process.env.LIFF_ID,
        APIGATEWAY_STAGE: process.env.APIGATEWAY_STAGE,
        AJAX_MODULE: process.env.AJAX_MODULE,
    }
}
