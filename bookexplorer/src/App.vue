<template>
  <v-app>
    <component v-bind:is="currentTabComponent" v-bind:username="username"></component>
  </v-app>
</template>


<script>
import login from './components/login';
import BExplorer from './components/BExplorer';
import {eventBus} from './main.js';

export default {
  name: 'App',

  components: {
    login,
    BExplorer
  },

  data: () => ({
    currentTab: "login",
    username: null,

  }),
  mounted() {
    eventBus.$on("log-in", data => {
      this.currentTab = data.tab; 
      this.username = data.user;
    });

    eventBus.$on("log-out", data => {
      this.currentTab = data; 
      this.username = null;
    });
  },
  computed: {
    currentTabComponent() {
      return this.currentTab;
    }
  },
}
</script>
