import Vue from 'vue';
import Router from 'vue-router';
import HomeView from '@/components/HomeView.vue';
import ProductosList from '@/components/ProductosList.vue';
import LoginView from '@/components/LoginView.vue';

Vue.use(Router);

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView,
  },
  {
    path: '/productos/lista',
    name: 'ProductosList',
    component: ProductosList,
  },
  {
    path: '/login',
    name: 'loginView',
    component: LoginView,
  },
];

const router = new Router({
  mode: 'history', // Usa el modo 'history' para URLs limpias
  routes,
});

export default router;
