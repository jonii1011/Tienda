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
  },
  mutations: {
    setAuth(state, { access, refresh, nombre, role }) {
      console.log('Actualizando estado: ', { access, refresh, nombre, role });
      state.isAuthenticated = true;
      state.nombreUsuario = nombre;
      state.accessToken = access;
      state.refreshToken = refresh;
      state.userRole = role;
    },
    clearAuth(state) {
      state.isAuthenticated = false;
      state.nombreUsuario = '';
      state.accessToken = '';
      state.refreshToken = '';
      state.userRole = ''; 
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
        });
    
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        localStorage.setItem('nombreUsuario', response.data.nombre);
        localStorage.setItem('userRole', response.data.role);
    
        console.log('Nombre de usuario guardado:', response.data.nombre);
        
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
        });
      } catch (error) {
        console.error('Error al obtener la información del usuario:', error);
      }
    },
    logout({ commit }) {
      commit('clearAuth');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('nombreUsuario');
      localStorage.removeItem('userRole');
    },
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    nombreUsuario: state => state.nombreUsuario,
    userRole: state => state.userRole,
    accessToken: state => state.accessToken,
    refreshToken: state => state.refreshToken,
  },
});






