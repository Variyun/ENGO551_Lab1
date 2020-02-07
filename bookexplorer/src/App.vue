<template>
  <v-app>
    <component v-bind:is="currentTabComponent"></component>
  </v-app>
</template>


<script>
import login from './components/login';
import BExplorer from './components/BExplorer';

export default {
  name: 'App',

  components: {
    login,
    BExplorer
  },

  data: () => ({
    loggedout: true,
    test: false,
    currentTab: "login"
  }),
  methods: {
    
  },
  computed: {
    currentTabComponent() {
      return this.currentTab.toLowerCase();
    }
  },
  props: {
   //
  }
}

</script>
