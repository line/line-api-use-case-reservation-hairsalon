<template>
    <v-app class="reserve-font-size">
        <!-- Header -->
        <v-app-bar app dense class="elevation-1" style="width:100%;" color="grey lighten-5">
            <v-toolbar-title style="width:100%;">
                 <v-chip outlined class="float-right">
                    <span class="info-hairsalon line-color">{{ area ? area.name : null }}&nbsp;&nbsp;{{ hairsalon ? hairsalon.name : null }}</span>
                </v-chip>
            </v-toolbar-title>
        </v-app-bar>
        <!-- Weekdays Header　-->
        <v-alert icon="info" outlined prominent border="left" class="mt-16 ma-2" style="color:#00ba00;">
            <span class="info-hairsalon"><span v-html="$t('staffs.msg001', { salon: hairsalon.name })"></span></span>
            <span class="float-right info-hairsalon-subtext mt-1" style="color:#FF8A80;">{{ $t("staffs.msg002") }}</span>
        </v-alert>
        <v-container fluid>
            <v-row justify="center" align-content="center">
                <v-col cols="6" sm="4" class="text-center" v-for="staff in staffs" v-bind:key="staff.staffId">
                    <div>
                        <v-avatar size="100" class="staff" v-on:click="showProfile(staff)">
                            <v-img v-bind:src="staff.img"></v-img>
                        </v-avatar>
                        <div v-if="staff.sex=='male'" v-on:click="showProfile(staff)">
                            <v-chip outlined color="blue lighten-1" class="staff elevation-6" style="color:white;">{{ staff.name }}</v-chip>
                        </div>
                        <div v-else-if="staff.sex=='female'" v-on:click="showProfile(staff)">
                            <v-chip outlined color="pink lighten-1" class="staff elevation-6" style="color:white;">{{ staff.name }}</v-chip>
                        </div>
                        <div v-else v-on:click="showProfile(staff)">
                            <v-chip outlined  color="deep-purple lighten-1" class="staff elevation-6" style="color:white;">{{ staff.name }}</v-chip>
                        </div>
                    </div>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
            <v-row style="height:36px;"></v-row>
        </v-container>
        <!-- Dialog -->
        <v-dialog v-model="dialog" max-width="300">
            <v-card style="border-radius:0;">
                <v-card-title class="pl-4 pr-0 pb-0">
                    <div style="width:100%;">
                        <div v-if="selectedStaff.sex=='male'">
                            <v-chip outlined left color="blue lighten-1" class="elevation-0">{{ $t("staffs.msg003", { career: selectedStaff.career}) }}</v-chip>
                            <span class="font-weight-bold ml-2" style="font-size:1.0em;">{{ selectedStaff.name }}</span>
                        </div>
                        <div v-else-if="selectedStaff.sex=='female'">
                            <v-chip outlined color="pink lighten-1" class="elevation-0">{{ $t("staffs.msg003", { career: selectedStaff.career}) }}</v-chip>
                            <span class="font-weight-bold ml-2" style="font-size:1.0em;">{{ selectedStaff.name }}</span>
                        </div>
                        <div v-else class="text-center mr-6">
                            <span class="font-weight-bold" style="font-size:1.0em;">{{ selectedStaff.name }}</span>
                        </div>
                    </div>
                    <v-btn icon style="position:absolute; right:0; top:0;" v-on:click="dialog=false">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-card-title>
                <v-card-title>
                    <v-img style="width:150px;" v-bind:src="selectedStaff.img" /><br/>
                </v-card-title>
                <v-card-actions>
                    <v-form ref="form" v-model="valid" lazy-validation style="width:96%; margin:0 auto;">
                        <v-select
                            dense
                            v-bind:label="$t('staffs.msg004')"
                            v-bind:items="menu"
                            item-text="text"
                            return-object
                            required
                            v-model="selectedMenu"
                            v-bind:rules="[v=>!!v || $t('staffs.msg005')]"
                        ></v-select>
                    </v-form>
                </v-card-actions>
                <v-card-subtitle class="pl-3 pr-3 pb-1" v-show="selectedStaff.staffId!=0">
                    <v-icon>mdi-comment</v-icon>
                    <span style="color:#000;">{{ $t("staffs.msg006") }}</span><br/>
                    <span style="margin:0 auto;">{{ selectedStaff.message }}</span>
                </v-card-subtitle>
            </v-card>
            <footer style="text-align:center; width:100%;">
                <v-btn 
                    class="ma-0 font-weight-bold"
                    style="width:100%; height:48px; background-color:#00ba00; border-radius:0 0 4px 4px;"
                    v-on:click="reserve(selectedStaff, selectedMenu)"
                >
                    <span style="color:#fff;">{{ $t("staffs.msg007") }}</span>
                </v-btn>
            </footer>
        </v-dialog>
        <!-- Footer -->
        <vue-footer icons="2" v-bind:shop="hairsalon.id"></vue-footer>
    </v-app>
</template>

<script>
/**
 * スタッフ選択画面
 * 
 */
import VueFooter from "~/components/hairsalon/Footer.vue"

export default {
    layout: "reserve/hairsalon",
    components: {
        VueFooter,
    },
    async asyncData({ app, params, store }) {
        // 対象店舗取得
        let area = app.$flash.hold("area");
        let hairsalon = app.$flash.hold("hairsalon");
        // リロード対応
        if (area === undefined) { 
            const data = await app.$hairsalon.getAreaShops();
            area = data.areas.find((v) => v.code == params.code);
            hairsalon = data.hairsalons[params.code].find((v) => v.id == params.id);
        }
        // スタッフ取得 (Call Backend Lambda)
        const staffsPromise = app.$hairsalon.getShopStaffs(hairsalon.id);
        // コースリスト取得
        const menuPromise = app.$hairsalon.getCourses(hairsalon.id);

        let staffs = await staffsPromise;
        let menu = await menuPromise;

        return {
            area: area,
            hairsalon: hairsalon,
            staffs: staffs,
            menu: menu,
        };
    },
    head() {
        return {
            title: this.$t("title")
        }
    },
    data() {
        return {
            area: null,
            hairsalon: null,
            staffs: null,
            menu: null,
            dialog: false,
            valid: true,
            selectedStaff: {
                staffId: null,
                name: null,
                sex: null,
                img: null,
                career: null,
                message: null,
            },
            selectedMenu: null,
        }
    },
    methods: {
        /**
         * プロフィール表示
         * 
         * @param {Object} staff スタッフ情報
         */
        showProfile(staff) {
            this.selectedStaff = staff;
            this.selectedMenu = null;
            setTimeout(()=>{
                this.$refs.form.resetValidation();
            }, 0);
            this.dialog = true;
        },

        /**
         * 予約カレンダー画面へ遷移
         * 
         * @param {Object} staff 指定スタッフ情報
         * @param {Object} menu 指定メニュー情報
         */
        reserve(staff, menu) {
            const ret = this.$refs.form.validate();
            if (!ret) return;

            const area = this.area;
            const hairsalon = this.hairsalon;
            this.$flash.set("area", area);
            this.$flash.set("hairsalon", hairsalon);
            this.$flash.set("staff", staff);
            this.$flash.set("menu", menu);
            this.$router.push(`/hairsalon/${area.code}/${hairsalon.id}/${staff.staffId}`);
        },
    }

}
</script>

<style scoped>
.v-chip:before {
    background-color: transparent;
}
.hairsalon-title {
    font-size: 16px;
    letter-spacing: 0.06em;
}
.staff {
    cursor: pointer;
}
.reserve-font-size {
    font-size: 16px;
    width: auto;
}
.info-hairsalon {
    font-size:1.2em;
}
.info-hairsalon-subtext {
    font-size: 1.0em;
}
@media screen and (max-width:540px) {
    .reserve-font-size {
        font-size: 12px;
    }
    .info-hairsalon {
        font-size:1.0em;
    }
    .info-hairsalon-subtext {
        font-size: 0.8em;
    }
}
</style>
