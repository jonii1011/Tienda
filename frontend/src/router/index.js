import Vue from 'vue';
import Router from 'vue-router';
import HomeView from '@/components/HomeView.vue';
import ProductosList from '@/components/ProductosList.vue';
import LoginView from '@/components/LoginView.vue';
import RegistrarCliente from '@/components/RegistrarCliente.vue';
import GestionProductos from '@/components/GestionProductos.vue';
import store from '@/store';
import PerfilView from '@/components/PerfilView.vue';
import GestionModelo from '@/components/GestionModelo.vue';
import CarritoView from '@/components/CarritoView.vue';
import VentasView from '@/components/VentasView.vue';
import ContactoView from '@/components/ContactoView.vue';

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
  {
    path: '/cliente-registrar',
    name: 'RegistrarCliente',
    component: RegistrarCliente,
  },
  {
    path: '/GestionProductos',
    name: 'GestionProductos',
    component: GestionProductos,
    meta: { requiresAuth: true }, // Ruta protegida
    props: true,
  },
  {
    path: '/perfil',
    name: 'PerfilView',
    component: PerfilView,
    meta: { requiresAuth: true }, // Ruta protegida
  },
  {
    path: '/modelo',
    name: 'GestionModelo',
    component: GestionModelo,
    meta: { requiresAuth: true }, // Ruta protegida
  },
  {
    path: '/carrito',
    name: 'CarritoView',
    component: CarritoView,
    meta: { requiresAuth: true }, // Ruta protegida
  },
  {
    path: '/ventas',
    name: 'VentasView',
    component: VentasView,
    meta: { requiresAuth: true }, // Ruta protegida
  },
  {
    path: '/contacto',
    name: 'ContactoView',
    component: ContactoView,
  },
];


const router = new Router({
  mode: 'history', // Usa el modo 'history' para URLs limpias
  routes,
});

// Guard para verificar la autenticación
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated; // Obtén el estado de autenticación del store

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'loginView' }); // Redirige a login si no está autenticado
  } else {
    next(); // Permite el acceso a la ruta
  }
});

export default router;
