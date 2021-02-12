<template>
<div>
    <v-dialog v-model="axiosError" persistent max-width="500">
        <v-card>
            <v-card-title>
                <v-icon large color="error">error</v-icon>{{ $t("error.msg001") }}
                <v-btn absolute right icon v-on:click="close">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-card-title>
            <v-card-text>
                <p><span v-html="$t('error.msg002')"></span></p>
                <p>（{{ $t("error.msg003") }}：{{axiosError}}）</p>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" text @click="reload">{{ $t("error.msg004") }}</v-btn>
                <v-spacer></v-spacer>
            </v-card-actions>
        </v-card>
    </v-dialog>
</div>
</template>
<script>
/**
 * 通信エラーダイアログ
 * 
 */
import {mapGetters} from 'vuex'

export default {
    computed:{
        ...mapGetters(['axiosError', 'isAxiosError']),
    },
    methods: {
        /**
         * 画面リロード処理
         * 
         */
        reload() {
            location.reload();
            return;
        },

        /**
         * 画面非表示処理
         * 
         */
        close() {
            this.$store.commit("axiosError", null);
        }
    }
}
</script>