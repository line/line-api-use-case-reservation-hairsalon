<template>
    <v-app class="font-size" v-bind:style="style">
        <h1 class="message">404 Not Found</h1>
    </v-app>
</template>

<script>
/**
 * HTTP 404 Error Page 
 * 
 */
export default {
    data() {
        return {
            style: {
                backgroundImage: "url(https://media.istockphoto.com/photos/error-picture-id1157134529)",
                backgroundRepeat: "no-repeat",
                backgroundSize: "cover",
                backgroundPosition: "center center"
            },
        }
    }
}
</script>

<style scoped>
.message {
    margin: 36px auto;
    color: black;
    text-shadow: 2px 3px 3px #fff;
}
.font-size {
    font-size: 24px;
}
@media screen and (max-width:540px) {
    .font-size {
        font-size: 18px;
    }
}
</style>
