import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import axios from 'axios'

Vue.config.productionTip = false
//constant variable eventbus
export const eventBus = new Vue();

new Vue({
  vuetify,
  axios,
  render: h => h(App)
}).$mount('#app')
