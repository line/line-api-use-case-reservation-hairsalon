<template>
    <v-app class="reserve-font-size">
        <v-expansion-panels class="mb-14">
            <v-container>
                <v-row>
                    <p>test</p>
                    <p>{{ areas }}</p>
                </v-row>
            </v-container>
        </v-expansion-panels>
        <!-- Footer -->
        <vue-footer icons="1"></vue-footer>
    </v-app>
</template>
<script>
import VueFooter from "~/components/hairsalon/Footer.vue"

export default {
    layout: "reserve/hairsalon",
    components: {
        VueFooter,
    },
    async asyncData({ app }) {
        const data = await app.$hairsalon.getAreaShops()
        const areas = data.areas
        const hairsalons = data.hairsalons
        return {
            areas: areas,
            hairsalons: hairsalons,
        }
    },
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
    font-size: 1.2em;
}
.info-hairsalon-subtext {
    font-size: 1em;
}
@media screen and (max-width: 540px) {
    .reserve-font-size {
        font-size: 12px;
    }
    .info-hairsalon {
        font-size: 1em;
    }
    .info-hairsalon-subtext {
        font-size: 0.8em;
    }
}
</style>
