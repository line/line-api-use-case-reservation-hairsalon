<template>
    <v-app class="reserve-font-size">
        <v-expansion-panels class="mb-14">
            <v-container>
                <v-row>
                    <v-expansion-panel v-for="area in areas" v-bind:key="area.code">
                        <v-expansion-panel-header color="white" style="opacity:0.8;">
                            <div class="font-weight-bold" style="font-size:1.0rem;">
                                <span class="text-area">{{ area.name }}</span>
                            </div>
                        </v-expansion-panel-header>
                        <v-expansion-panel-content color="grey lighten-5">
                            <v-container>
                                <v-row>
                                    <v-col cols="12" sm="6" md="4" v-for="hairsalon in hairsalons[area.code]" v-bind:key="hairsalon.id">
                                        <v-hover v-slot:default="{ hover }" open-delay="150">
                                            <v-card outlined class="hairsalon" v-bind:elevation="hover ? 16 : 2" v-bind:ripple="rippled" v-on:mousedown.capture="mousedownCard(1)" v-on:click="reserve(area, hairsalon)">
                                                <v-list-item-title class="mt-1 ml-1">
                                                    <span style="font-size:1.2em;">{{ hairsalon.name }}</span>
                                                </v-list-item-title>
                                                <v-list-item class="ma-0 pa-0">
                                                    <v-img class="ma-1" style="width:50%;" v-bind:src="hairsalon.img" alt="LINE Shop" />
                                                    <v-sheet class="ma-1 pa-2" style="width:50%; font-size:0.7em; background-color:transparent;">
                                                        <ul class="ma-0 pa-1">
                                                            <li class="pb-1">{{ $t("areas.msg001") }}: {{ hairsalon.start }}～{{ hairsalon.end }}</li>
                                                            <li class="pb-1">{{ $t("areas.msg002") }}: {{ weekdayNames(hairsalon.holiday) }}</li>
                                                            <li class="pb-1" v-if="hairsalon.line">
                                                                <a href="javascript:void(0);"
                                                                   v-bind:style="lineIcon"
                                                                    v-on:mousedown="mousedownCard(2)"
                                                                    v-on:click.stop="openLineOA(hairsalon.line)"
                                                                >
                                                                    {{ $t("areas.msg003") }}
                                                                </a>
                                                            </li>
                                                            <li class="pb-1" v-else-if="!hairsalon.line">Mail: {{ hairsalon.email }}</li>
                                                            <li class="pb-1">Tel: {{ hairsalon.tel }}</li>
                                                        </ul>
                                                    </v-sheet>
                                                </v-list-item>
                                                <v-list-item-action-text>
                                                    <p class="ma-0" style="font-size:1.0em; color:gray;">
                                                        <v-icon>mdi-map-marker</v-icon>
                                                        <a href="javascript:void(0);"
                                                           v-bind:style="mapIcon"
                                                           v-on:mousedown="mousedownCard(2)"
                                                           v-on:click.stop="openMap(hairsalon.name, hairsalon.map)"
                                                        >
                                                            {{ hairsalon.address }}
                                                        </a>
                                                    </p>
                                                </v-list-item-action-text>
                                            </v-card>
                                        </v-hover>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-row>
            </v-container>
        </v-expansion-panels>
        <!-- Footer -->
        <vue-footer icons="1"></vue-footer>
    </v-app>
</template>

<script>
/**
 * エリア・店舗選択画面 
 * 
 */
import VueFooter from "~/components/hairsalon/Footer.vue"

export default {
    layout: "reserve/hairsalon",
    components: {
        VueFooter,
    },
    async asyncData({ app }) {
        // エリアデータ＆店舗データ取得 (Call Backend Lambda)
        const data = await app.$hairsalon.getAreaShops();
        const areas = data.areas;
        const hairsalons = data.hairsalons;

        return {
            areas: areas,
            hairsalons: hairsalons,
        };
    },
    head() {
        return {
            title: this.$t("title")
        }
    },
    data() {
        return {
            areas: null,
            hairsalons: null,
            reserved: false,
            rippled: false,
            icon: {
                line: require('~/assets/img/icon/line.png'),
                map: require('~/assets/img/icon/map.png')
            }
        }
    },
    computed: {
        lineIcon() {
            return `cursor:url(${this.icon.line}) 12 12, auto`;
        },
        mapIcon() {
            return `cursor:url(${this.icon.map}) 12 12, auto`;
        }
    },
    created() {

    },
    methods: {
        /**
         * 曜日名文字列
         * 
         * @param {Array<number>|string} weekdays 曜日情報
         * @returns {string} カンマ区切り曜日名
         */
        weekdayNames(weekdays) {
            let names = "";
            if (typeof(weekdays) == "object") {
                for (const weekday of weekdays) {
                    if (names.length > 0) { names += ", "; }
                    names += this.$utils.weekdayName(weekday);
                }
            } else {
                names = weekdays;
            }

            return (names.length == 0) ? this.$t("areas.msg004") : names;
        },

        /**
         * スタッフ選択画面へ遷移
         * 
         * @param {Array<Object>} area エリア情報
         * @param {Array<Object>} hairsalon ヘアサロン店舗情報
         */
        reserve(area, hairsalon) {
            this.$flash.set("area", area);
            this.$flash.set("hairsalon", hairsalon);
            this.$router.push(`/hairsalon/${area.code}/${hairsalon.id}`);
        },

        /**
         * 店舗カードマウスダウン処理
         * 
         * @param {number} num インデックス番号
         */
        mousedownCard(num) {
            const tagName = event.srcElement.tagName;
            if (num == 2) {
                event.stopPropagation();
            } else {
                if (tagName != "A") {
                    this.rippled = true;
                }
            }
        },

        /**
         * 地図を開く
         * 
         * @param {string} name 店舗名称
         * @param {Object} coordinate 緯度・経度
         */
        openMap(name, coordinate) {
            let latitude = coordinate.latitude;
            let longitude = coordinate.longitude;
            this.$utils.openMapApp(latitude, longitude, 18);
        },

        /**
         * LINE公式アカウントを開く
         * 
         * @param {string} LINE公式アカウント
         */
        openLineOA(line) {
            this.$utils.openLineOA(line);
        }
    }
}
</script>

<style scoped>
.text-area {
    color: #00ba00;
}
.map-title {
    color: #fff;
}
.hairsalon {
    cursor: pointer;
    padding: 4px;
}
.reserve-font-size {
    font-size: 16px;
    letter-spacing: 0.06em;
}
.hairsalon-header {
    font-size: 1.1em;
}
@media screen and (max-width:540px) {
    .reserve-font-size {
        font-size: 12px;
        letter-spacing: 0.06em;
    }
    .hairsalon-header {
        font-size: 1.0em;
    }
}
</style>
