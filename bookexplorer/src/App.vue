<template>
  <v-app>
    <login v-model="loggedout"/>
    <!-- <BExplorer/> -->
  </v-app>
</template>


<script>
import login from './components/login';
//import BExplorer from './components/BExplorer';

export default {
  name: 'App',

  components: {
    login,
    //BExplorer
  },

  data: () => ({
    loggedout: true,
    test: false
  }),

  props: {
   //
  }
};
</script>
