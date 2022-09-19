<template>
  <router-view />
  <router-link custom v-slot="{ navigate }" :to="{ name: 'AdminIndex' }">
    <button @click="navigate">Admin画面</button>
  </router-link>
  <router-link custom v-slot="{ navigate }" :to="{ name: 'ReserveList' }">
    <button @click="navigate">ReserveList</button>
  </router-link>
  <div v-if="isSignedIn">
    <amplify-greetings> </amplify-greetings>
  </div>
</template>

<script>
export default {
  computed: {
    isSignedIn() {
      return this.$store.state.user !== null;
    },
  },
};
</script>
