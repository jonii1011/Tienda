import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import router from './router'; // Asegúrate de que la ruta sea correcta

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isAuthenticated: !!localStorage.getItem('access_token'),
    nombreUsuario: localStorage.getItem('nombreUsuario') || '',
    accessToken: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
    userRole: localStorage.getItem('userRole') || '',
    userId: localStorage.getItem('userId') || '',
    carrito: [], // Agrega esta línea
  },
  mutations: {
    setAuth(state, { access, refresh, nombre, role, id }) {
      state.isAuthenticated = true;
      state.nombreUsuario = nombre;
      state.accessToken = access;
      state.refreshToken = refresh;
      state.userRole = role;
      state.userId = id;

      // Guardar en localStorage
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('nombreUsuario', nombre);
      localStorage.setItem('userRole', role);
      localStorage.setItem('userId', id);
    },
    clearAuth(state) {
      state.isAuthenticated = false;
      state.nombreUsuario = '';
      state.accessToken = '';
      state.refreshToken = '';
      state.userRole = ''; 
      state.userId = '';

      // Limpiar localStorage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('nombreUsuario');
      localStorage.removeItem('userRole');
      localStorage.removeItem('userId');
    },
    initializeStore(state) {
      // Inicializa el estado desde localStorage
      const access = localStorage.getItem('access_token');
      const refresh = localStorage.getItem('refresh_token');
      const nombre = localStorage.getItem('nombreUsuario');
      const role = localStorage.getItem('userRole');
      const id = localStorage.getItem('userId');

      if (access) {
        state.isAuthenticated = true;
        state.accessToken = access;
        state.refreshToken = refresh || '';
        state.nombreUsuario = nombre || '';
        state.userRole = role || '';
        state.userId = id || '';
      }
    },
    initializeCarrito(state) {
      const carrito = localStorage.getItem('carrito');
      if (carrito) {
        state.carrito = JSON.parse(carrito);
      }
    },
    agregarAlCarrito(state, producto) {
      const existingProduct = state.carrito.find(item => item.id_producto === producto.id_producto);
      if (existingProduct) {
        // Si el producto ya existe, aumenta la cantidad
        existingProduct.cantidad += 1;
      } else {
        // Si no existe, añade el producto con cantidad 1
        state.carrito.push({
          ...producto,
          cantidad: 1, // Inicializa la cantidad en 1
        });
      }
      // Guardar el carrito en localStorage
    localStorage.setItem('carrito', JSON.stringify(state.carrito));
    },
    limpiarCarrito(state) {
      state.carrito = [];
      localStorage.removeItem('carrito'); // Elimina el carrito de localStorage
    },
    AUMENTAR_CANTIDAD(state, productoId) {
      const producto = state.carrito.find(item => item.id_producto === productoId);
      if (producto) {
        producto.cantidad += 1;
        localStorage.setItem('carrito', JSON.stringify(state.carrito)); // Guarda en localStorage
      }
    },
    
    DISMINUIR_CANTIDAD(state, productoId) {
      const producto = state.carrito.find(item => item.id_producto === productoId);
      if (producto && producto.cantidad > 1) {
        producto.cantidad -= 1;
        localStorage.setItem('carrito', JSON.stringify(state.carrito)); // Guarda en localStorage
      }
    },
  },
  actions: {
    async login({ commit, dispatch }, { email, password }) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/token/', {
          email: email,
          password: password,
        });
    
        console.log('Respuesta del backend:', response.data);
    
        commit('setAuth', {
          access: response.data.access,
          refresh: response.data.refresh,
          nombre: response.data.nombre, // Asegúrate de que este campo exista
          role: response.data.role,
          id: response.data.id,
        });
        
        // Llama a la función para obtener la información del usuario
        await dispatch('obtenerInformacionUsuario');

        // Redirigir a la página de inicio después de iniciar sesión
        router.push({ name: 'HomeView' });

        return true;
      } catch (error) {
        console.error('Error en la acción de login:', error.response ? error.response.data : error.message);
        throw error.response ? error.response.data.detail : 'Error en la conexión';
      }
    },
    async obtenerInformacionUsuario({ commit }) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:8000/auth/status/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        console.log('Información del usuario:', response.data);
        // Actualiza el estado de Vuex con la información del usuario
        commit('setAuth', {
          access: token,
          refresh: localStorage.getItem('refresh_token'),
          nombre: response.data.nombre,
          role: response.data.role,
          id: response.data.id,
        });
      } catch (error) {
        console.error('Error al obtener la información del usuario:', error);
      }
    },
    logout({ commit }) {
      commit('clearAuth');
      commit('limpiarCarrito'); // Limpia el carrito
    },
    agregarAlCarrito({ commit }, producto) {
      commit('agregarAlCarrito', producto);
    },
    vaciarCarrito({ commit }) {
      commit('limpiarCarrito');
    },
    initializeStore({ commit }) {
      commit('initializeStore'); // Inicializa el estado de autenticación
      commit('initializeCarrito'); // Inicializa el carrito
    },
    aumentarCantidad({ commit }, productoId) {
      commit('AUMENTAR_CANTIDAD', productoId);
    },
    disminuirCantidad({ commit }, productoId) {
      commit('DISMINUIR_CANTIDAD', productoId);
    },
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    nombreUsuario: state => state.nombreUsuario,
    userRole: state => state.userRole,
    accessToken: state => state.accessToken,
    refreshToken: state => state.refreshToken,
    userId: state => state.userId,
    carrito: state => state.carrito,
    cantidadCarrito: state => {
      return state.carrito.reduce((total, producto) => total + producto.cantidad, 0);
    },
  },
});







