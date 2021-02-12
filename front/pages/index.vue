<template>
    <v-app>
        <img src="https://media.istockphoto.com/photos/beauty-saloon-interior-visualization-3d-illustration-picture-id1065779636" alt="Hairsalon" style="width:100%;">
        <div style="color: #555; margin-top: 20px;" class="mx-5">
            <span style="border-left: 12px solid #16C464; padding:0 15px; color: #555" class="text-h5">{{ $t("top.title") }}</span>
            <ul class="text-body-2 mt-5">
                <li>{{ $t("top.msg001") }}</li>
                <li>{{ $t("top.msg002") }}</li>
            </ul>
        </div>
        <div style="line-height: 1.2em; margin-bottom: 70px;" class="mt-5 pa-2">
            <div style="font-size: 0.75em; color:#7c7c7c;" class="mx-5 mb-0">
                {{ $t("top.msg003") }}<br />
                {{ $t("top.msg004") }}<br />
                <br />
                {{ $t("top.msg005") }}
            </div>
        </div>
        <!-- ボタン -->
        <v-footer fixed style="" class="pa-0" height="60px">
            <v-btn class="basket text-h5 font-weight-bold" color="#00B900" v-on:click="reserve" style="color:#fff; width:100%; height:100%;">
                <span v-html="$t('top.msg006')"></span><v-icon large>keyboard_arrow_right</v-icon>
            </v-btn>
        </v-footer>
    </v-app>
</template>

<script>
/**
 * トップページ
 * 
 */
export default {
    layout: "reserve/hairsalon",
    head() {
        return {
            title: this.$t("title")
        }
    },
    methods: {
        /**
         * エリア・店舗選択画面へ遷移
         * 
         */
        reserve() {
            this.$router.push("/hairsalon/areas");
        },
    }
}
</script>

<style scoped>
html, body {
    margin: 0;
    width: 100%;
    height: 100%;
}
li {
    margin-top: 20px;
}
</style>
