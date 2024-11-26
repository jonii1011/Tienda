import Vue from 'vue'
import App from './App.vue'
import router from './router';
import vuetify from './plugins/vuetify'
import 'vuetify/dist/vuetify.min.css';
import store from './store';

Vue.config.productionTip = false
store.commit('initializeStore');

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
